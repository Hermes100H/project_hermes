using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BarScript : MonoBehaviour
{
    public Slider bar;
    public float barValue;
    public bool modePlayable;
    public float barScale = 0.001f;
    public controller optimController;
    // Start is called before the first frame update
    void Start()
    {
        bar = GetComponent<Slider>();
        bar.value = 10f;
        RectTransform sliderRectTransform = bar.GetComponent<RectTransform>();

        if(optimController.indexCircuit == 0)
        {
            sliderRectTransform.localScale = new Vector3(0.08f, 0.08f, 1f);
            sliderRectTransform.anchoredPosition = new Vector3(0.0f, -6f, 0.0f);
        }

        else if(optimController.indexCircuit == 1)
        {
            sliderRectTransform.localScale = new Vector3(0.02f, 0.02f, 1f);
            sliderRectTransform.anchoredPosition = new Vector3(0.0f, -2f, 0.0f);
        }

        else if (optimController.indexCircuit == 2)
        {
            sliderRectTransform.localScale = new Vector3(0.5f, 0.5f, 1f);
            sliderRectTransform.anchoredPosition = new Vector3(0.0f, -35f, 0.0f);   
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (!modePlayable)
        {
            bar.value = barValue;
        }
        else
        {
            float horizontalInput = Input.GetAxis("Horizontal");
            bar.value += horizontalInput * Time.deltaTime * 10f;
            barValue = bar.value;
        }
    }
}
