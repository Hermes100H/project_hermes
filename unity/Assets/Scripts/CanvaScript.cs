using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CanvaScript : MonoBehaviour
{
    public controller optimController;
    // Start is called before the first frame update
    void Start()
    {
        RectTransform canvasRectTransform = GetComponent<RectTransform>();
        
        if(optimController.indexCircuit == 0)
        {
            transform.position = new Vector3(12f, 4.6f, 0.0f);

            float width = 33;
            float height = 16;

            canvasRectTransform.sizeDelta = new Vector2(width, height);
        }

        else if(optimController.indexCircuit == 1)
        {
            transform.position = new Vector3(4.04f, 0.55f, 0.0f);

            float width = 11;
            float height = 5;

            canvasRectTransform.sizeDelta = new Vector2(width, height);
        }

        else if (optimController.indexCircuit == 2)
        {
            canvasRectTransform.position = new Vector3(70f, 20f, 0f);
            
            float width = 210;
            float height = 100;

            canvasRectTransform.sizeDelta = new Vector2(width, height);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
