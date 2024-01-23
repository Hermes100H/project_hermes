using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CamScript : MonoBehaviour
{
    public controller optimController;
    public float size;
    
    // Start is called before the first frame update
    void Start()
    {
        if (optimController.indexCircuit == 0)
        {
            transform.position = new Vector3(12f, 4.6f, -10.0f);
            Camera.main.orthographicSize = 8f;
        }

        else if(optimController.indexCircuit == 1)
        {
            transform.position = new Vector3(4f, 0.6f, -10f);
            Camera.main.orthographicSize = 2.6f;
        }

        else if(optimController.indexCircuit == 2)
        {
            transform.position = new Vector3(70, 20, -10);
            Camera.main.orthographicSize = 50;
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
