using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RaceTimesScript : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnGUI()
    {
        GUIStyle style = new GUIStyle();
        style.fontSize = 24;
        style.normal.textColor = Color.white;

        GUI.Label(new Rect(700, 85, 700, 180), "Ghost : 05:03", style);
    }
}
