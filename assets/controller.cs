using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class controller : MonoBehaviour
{
    public ReadingCSV csv;
    public List<float> cumulated_timing = new List<float>();
    public List<float> cumulated_energy = new List<float>();
    public List<Vector3> position = new List<Vector3>();
    public float energy_totale;
    public float energy_spent_frame;
    float time_simu;

    void Awake ()
    {
        csv = new ReadingCSV();
        cumulated_energy.Add(csv.energy[0]);
        cumulated_timing.Add(csv.timings[0]);
        position.Add(new Vector3(0.0f, 0.0f, 0.0f));
        
        for (int i = 1; i<csv.timings.Count; i++){
            cumulated_energy.Add(csv.energy[i] + cumulated_energy[i-1]);
            cumulated_timing.Add(csv.timings[i] + cumulated_timing[i-1]);
            position.Add(new Vector3(csv.DX[i-1], csv.DY[i-1], 0.0f) + position[i-1]);
        }
        position.Add(new Vector3(csv.DX[^1], csv.DY[^1], 0.0f) + position[^1]);
        energy_totale = cumulated_energy[^1];
    }

    
    void Update(){
        float delta_t = Time.deltaTime;
        float energy_previous = EnergyLeft(time_simu);
        float energy_next_step = EnergyLeft(time_simu+delta_t);
        energy_spent_frame = energy_previous - energy_next_step;
        time_simu += delta_t;
    }

    int GetIndexSegment(float t){
        if(t < cumulated_timing[0] & 0.0f < t){
            return 0;
        }
        for (int i = 1; i<cumulated_timing.Count; i++){
            if(cumulated_timing[i-1] < t & t < cumulated_timing[i]){
                return i;
            }
        }
        return -1;
    }

    public float EnergyLeft(float t) {
        int index = GetIndexSegment(t);
        if(index == -1){
            return 0.0f;
        }
        else{
            float temps_reduit_on_segment = 0;
            if(index == 0){
                temps_reduit_on_segment = t/csv.timings[index];
            }
            else {
                temps_reduit_on_segment = (t - cumulated_timing[index-1])/csv.timings[index];
            }
            float energy_segment = csv.energy[index];
            float energy_left = energy_totale - (cumulated_energy[index] - (1-temps_reduit_on_segment)*csv.energy[index]); 
            return energy_left;
        }
    }
}
