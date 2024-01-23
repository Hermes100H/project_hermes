using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PressSpaceScript : MonoBehaviour
{
    public controller optimController;
    public string text;
    public GhostScript ghost;
    public CarScript car;
    // Start is called before the first frame update
    void Start()
    {
        text = "Press Space to Start the Game";
    }

    // Update is called once per frame
    void Update()
    {
        if (optimController.gameStarted && car.gameOver == false)
        {
            text = "";
        }

        else if (car.gameOver == true && ghost.gameOver == true)
        {
            text = "Press Echap to return to the Main Menu";
        }
    }

    void OnGUI()
    {
        // Display the timer on the top left corner of the screen
        GUIStyle style = new GUIStyle();
        style.fontSize = 24;
        style.normal.textColor = Color.black;

        GUI.Label(new Rect(400, 500, 700, 180), text, style);
    }
}
    
