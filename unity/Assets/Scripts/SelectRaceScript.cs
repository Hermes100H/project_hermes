using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class SelectRaceScript : MonoBehaviour
{
    public Button startButton;
    public TitleScript title;
    public Button selectRaceButton;
    public Button race1button;
    public RaceTimesScript race1timer;
    // Start is called before the first frame update
    void Start()
    {
        race1button.gameObject.SetActive(false);
        race1timer.gameObject.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SelectRace()
    {
        RectTransform startButtonTransform = startButton.GetComponent<RectTransform>();
        startButtonTransform.anchoredPosition = new Vector3(0f, -3f, 0f);

        RectTransform selectRaceTransform = selectRaceButton.GetComponent<RectTransform>();
        selectRaceTransform.anchoredPosition = new Vector3(100f, 0f, 0f);

        race1button.gameObject.SetActive(true);
        race1timer.gameObject.SetActive(true);

        title.text = "";
    }
}
