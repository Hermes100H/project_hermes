using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class TitleScript : MonoBehaviour
{
    public string text;
    // Start is called before the first frame update
    void Start()
    {
        text = "Projet Hermes";
    }
        void OnGUI()
    {
        // Display the timer on the top left corner of the screen
        GUIStyle style = new GUIStyle();
        style.fontSize = 24;
        style.normal.textColor = Color.white;

        GUI.Label(new Rect(500, 150, 700, 180), text, style);
    }
}
