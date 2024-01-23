using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Race1Script : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        ParameterHolder.index = 0;
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Race1()
    {
        ParameterHolder.index = 1;
    }
}
