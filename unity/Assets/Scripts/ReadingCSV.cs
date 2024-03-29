using System.Collections;
using UnityEngine;
using System.IO;
using System.Collections.Generic;
using System.Globalization;
using System;

public class ReadingCSV : MonoBehaviour
{
    public List<float> timings = new List<float>();
    public List<float> boost_profile = new List<float>();
    public List<float> energy = new List<float>();
    public List<float> DX = new List<float>();
    public List<float> DY = new List<float>();
    public int indexCircuit;

    public void Init() 
    {
        timings.Clear();
        boost_profile.Clear();
        energy.Clear();
        DX.Clear();
        DY.Clear();

        indexCircuit = ParameterHolder.index;

        string path = "circuit" + indexCircuit.ToString() + ".csv";
        var reader = new StreamReader(File.OpenRead(@"Assets/Circuits/" + path));

        int i = 0;
        while (!reader.EndOfStream) {
            var line = reader.ReadLine();
            if (i==0){
                line = reader.ReadLine();
                i+=1;
            }
            var values = line.Split(',');
            boost_profile.Add(float.Parse(values[0], CultureInfo.InvariantCulture));
            timings.Add(float.Parse(values[1], CultureInfo.InvariantCulture));
            energy.Add(float.Parse(values[2], CultureInfo.InvariantCulture));
            DX.Add(float.Parse(values[3], CultureInfo.InvariantCulture));
            DY.Add(float.Parse(values[4], CultureInfo.InvariantCulture));
        }
    }
}
