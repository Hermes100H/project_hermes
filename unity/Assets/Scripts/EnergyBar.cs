using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class EnergyBar : MonoBehaviour{

    private Image barBorderImage;
    private RawImage barRawImage;
    public Energy energy;
    private RectTransform barMaskRectTransform;
    private float fluidSpeed = .1f;
    private float barMaskHeight;
    public controller optimController;
    public CarScript car;

    private void Start()
    {
        barMaskRectTransform = transform.Find("barMask").GetComponent<RectTransform>();
        barRawImage = transform.Find("barMask").Find("bar").GetComponent<RawImage>();
        energy = new Energy(optimController.energy_totale, optimController, car);
        barMaskHeight = barMaskRectTransform.sizeDelta.y;
        barBorderImage = transform.Find("border").GetComponent<Image>();
        
        if(optimController.indexCircuit == 0)
        {
            transform.position = new Vector3(-21f, -3f, 0f);
            transform.localScale = new Vector3(0.02f, 0.02f, 1f);
        }

        else if(optimController.indexCircuit == 1)
        {
            transform.position = new Vector3(-4.8f, 0.5f, 0f);
            transform.localScale = new Vector3(0.006f, 0.006f, 1f);
        }

        else if (optimController.indexCircuit == 2)
        {
            transform.position = new Vector3(-98f, -23f, 0f);
            transform.localScale = new Vector3(0.1f, 0.1f, 1f);
        }
    }


    // Update is called once per frame
    private void Update(){
        energy.Update();
        RenderEnergyFluidFalling();
        ResizeEnergyRemaining();
        barBorderImage.color = GetBorderColor(energy.GetNormalizedEnergy());
    }


    private void RenderEnergyFluidFalling(){

        Rect uvRect = barRawImage.uvRect;
        uvRect.y += fluidSpeed*Time.deltaTime;
        barRawImage.uvRect = uvRect;
    }


    private void ResizeEnergyRemaining(){

        Vector2 barMaskSizeDelta = barMaskRectTransform.sizeDelta;
        barMaskSizeDelta.y = energy.GetNormalizedEnergy() * barMaskHeight;
        barMaskRectTransform.sizeDelta = barMaskSizeDelta;
    }


    private Color GetBorderColor(float energyRemaining){

        Color blueColor = Color.blue;
        Color orangeColor = new Color(1f, 0.5f, 0f);
        Color redColor = Color.red;

        // Interpolate between red and orange
        Color lerpedColor1 = Color.Lerp(redColor, orangeColor, Mathf.InverseLerp(0, 0.5f, energyRemaining));
        // Interpolate between orange and blue
        Color lerpedColor2 = Color.Lerp(orangeColor, blueColor, Mathf.InverseLerp(0.5f, 1f, energyRemaining));
        // Final interpolation between the two intermediate colors
        Color finalLerpedColor = Color.Lerp(lerpedColor1, lerpedColor2, Mathf.InverseLerp(0, 1f, energyRemaining));

        return finalLerpedColor;
    }

}

public class Energy{

    private float totalEnergy = 100.0f;
    public float energyRemaining;
    public controller optimController;
    public CarScript car;

    public Energy(float pTotalEnergy, controller c, CarScript pCar){
        totalEnergy = pTotalEnergy;
        optimController = c;
        energyRemaining = pTotalEnergy;
        car = pCar;
    }

    public Energy(){
        energyRemaining = totalEnergy;
    }

    public void SpendEnergy(float amount){
        float amountAllowed = Mathf.Min(amount, energyRemaining);
        energyRemaining -= amountAllowed;
        
    }

    public float GetNormalizedEnergy(){
        return energyRemaining / totalEnergy;
    }


    public void Update()
    {
        SpendEnergy(car.energySpend);
    }
}
