using UnityEngine;

public class TimerScript : MonoBehaviour
{
    public float timer = 0f;
    public bool run = true;
    public int select;

    void Update()
    {
        // Update the timer every frame
        if (run)
        {
            timer += Time.deltaTime;
        }
    }

    void OnGUI()
    {
        // Display the timer on the top left corner of the screen
        if (select == 1)
        {
            GUIStyle style = new GUIStyle();
            style.fontSize = 24;
            style.normal.textColor = Color.black;

            GUI.Label(new Rect(10, 10, 200, 30), "Player Timer : " + timer.ToString("F2"), style);
        }
        if (select == 0)
        {
            GUIStyle style = new GUIStyle();
            style.fontSize = 24;
            style.normal.textColor = Color.black;

            GUI.Label(new Rect(10, 50, 200, 80), "Ghost Timer : " + timer.ToString("F2"), style);
        }
    }
}