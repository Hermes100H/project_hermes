// using System.Collections;
// using System.Collections.Generic;
// using UnityEngine;

// public class CarScript : MonoBehaviour
// {
//     // Start is called before the first frame update
//     public Vector3 startPosition;
//     public float startRotation;
//     public List<Vector3> positionList;
//     public List<float> speedList;
//     public List<float> rotationList;
//     public float g = 9.81f;
//     public List<Vector3> positionCircuit;
//     public List<float> accelerationProfile;
//     public List<float> accelerationList;
//     public TimerScript timer;
//     public bool modePlayable;
//     public BarScript accelerationBar;
//     public controller optimController;
//     public float upset;
//     public float energySpend;

//     void Start()
//     {
//         Init();
//     }

//     void Init()
//     {
//         positionCircuit = optimController.position;
//         accelerationProfile = optimController.csv.boost_profile;
//         modePlayable = optimController.modePlayable;
//         accelerationBar.modePlayable = modePlayable;
//         float theta = startRotation * (Mathf.PI/180);
//         transform.rotation = Quaternion.AngleAxis(startRotation, new Vector3(0,0,1));
//         positionList.Add(startPosition);
//         rotationList.Add(startRotation);
//         accelerationList.Add(accelerationProfile[0]);
//         speedList.Add(0f);

//         if(optimController.indexCircuit == 0)
//         {
//             transform.localScale = new Vector3(4f, 4f, 0f);
//             upset = 0.25f;
//         }

//         else if(optimController.indexCircuit == 1)
//         {
//             transform.localScale = new Vector3(2f, 2f, 0f);
//             upset = 0.1f;
//         }
//         transform.position = new Vector3(startPosition[0] - upset * Mathf.Sin(theta), startPosition[1] + upset *Mathf.Cos(theta), 0f);
//     }

//     // Update is called once per frame
//     void Update()
//     {
//         if (!modePlayable)
//         {
//             if ((positionList[positionList.Count-1][0] < positionCircuit[positionCircuit.Count-2][0]) && (positionList[positionList.Count-1][0] >= positionCircuit[0][0]))
//             {
//                 float xk = positionList[positionList.Count-1][0];
//                 float yk = positionList[positionList.Count-1][1];
//                 float vk = speedList[speedList.Count-1];
//                 float thetak = rotationList[rotationList.Count-1] * (Mathf.PI/180);
//                 float t = Time.deltaTime;
//                 float Fp = accelerationList[accelerationList.Count-1];
//                 accelerationBar.barValue = Fp;
//                 float x = ((-g/2) * Mathf.Cos(thetak) * Mathf.Sin(thetak) + Fp * Mathf.Cos(thetak)) * Mathf.Pow(t,2) + vk * Mathf.Cos(thetak) * t + xk;
//                 float y = ((g/2) * Mathf.Pow(Mathf.Cos(thetak),2) + Fp * Mathf.Sin(thetak)) * Mathf.Pow(t,2) - (g/2) * Mathf.Pow(t,2) + vk * t * Mathf.Sin(thetak) + yk;
//                 positionList.Add(new Vector3(x,y,0f));
//                 int count = 0;
//                 for (int i = 0; i < positionCircuit.Count; i++)
//                 {
//                     if (x > positionCircuit[i][0])
//                     {
//                         count = i;
//                     }
//                 }
//                 Fp = accelerationProfile[count];
//                 accelerationList.Add(Fp);
//                 if (count != positionCircuit.Count)
//                 {
//                     rotationList.Add((180/Mathf.PI) * Mathf.Atan((positionCircuit[count+1][1]-positionCircuit[count][1])/(positionCircuit[count+1][0]-positionCircuit[count][0])));
//                 }
//                 float theta = rotationList[rotationList.Count-1] * Mathf.PI/180;
//                 float sign = Mathf.Sign(t * (-g * Mathf.Cos(theta) * Mathf.Sin(theta) + Fp * Mathf.Cos(theta)) + vk * Mathf.Cos(theta));
//                 speedList.Add(sign * Mathf.Sqrt(Mathf.Pow(t * (-g  * Mathf.Cos(theta) * Mathf.Sin(theta) + Fp * Mathf.Cos(theta)) + vk *Mathf.Cos(theta),2) + Mathf.Pow(t * (-g + g * Mathf.Pow(Mathf.Cos(theta),2) + Fp * Mathf.Sin(theta)) + vk * Mathf.Sin(theta),2)));
//                 transform.position = new Vector3(positionList[positionList.Count-1][0] - upset * Mathf.Sin(theta), positionList[positionList.Count-1][1] + upset*Mathf.Cos(theta), 0f);
//                 transform.rotation = Quaternion.AngleAxis(rotationList[rotationList.Count-1], new Vector3(0,0,1));
//             }
//             else
//             {
//                 timer.run = false;
//             }
//         }

//         if (modePlayable)
//         {
//             if ((positionList[positionList.Count-1][0] < positionCircuit[positionCircuit.Count-2][0]) && (positionList[positionList.Count-1][0] >= positionCircuit[0][0]))
//             {
//                 float xk = positionList[positionList.Count-1][0];
//                 float yk = positionList[positionList.Count-1][1];
//                 float vk = speedList[speedList.Count-1];
//                 float thetak = rotationList[rotationList.Count-1] * (Mathf.PI/180);
//                 float t = Time.deltaTime;
//                 float Fp = accelerationBar.barValue;
//                 float x = ((-g/2) * Mathf.Cos(thetak) * Mathf.Sin(thetak) + Fp * Mathf.Cos(thetak)) * Mathf.Pow(t,2) + vk * Mathf.Cos(thetak) * t + xk;
//                 float y = ((g/2) * Mathf.Pow(Mathf.Cos(thetak),2) + Fp * Mathf.Sin(thetak)) * Mathf.Pow(t,2) - (g/2) * Mathf.Pow(t,2) + vk * t * Mathf.Sin(thetak) + yk;
//                 positionList.Add(new Vector3(x,y,0f));
//                 int count = 0;
//                 for (int i = 0; i < positionCircuit.Count; i++)
//                 {
//                     if (x > positionCircuit[i][0])
//                     {
//                         count = i;
//                     }
//                 }
//                 if (count != positionCircuit.Count)
//                 {
//                     rotationList.Add((180/Mathf.PI) * Mathf.Atan((positionCircuit[count+1][1]-positionCircuit[count][1])/(positionCircuit[count+1][0]-positionCircuit[count][0])));
//                 }
//                 float theta = rotationList[rotationList.Count-1] * Mathf.PI/180;
//                 float sign = Mathf.Sign(t * (-g * Mathf.Cos(theta) * Mathf.Sin(theta) + Fp * Mathf.Cos(theta)) + vk * Mathf.Cos(theta));
//                 speedList.Add(sign * Mathf.Sqrt(Mathf.Pow(t * (-g  * Mathf.Cos(theta) * Mathf.Sin(theta) + Fp * Mathf.Cos(theta)) + vk *Mathf.Cos(theta),2) + Mathf.Pow(t * (-g + g * Mathf.Pow(Mathf.Cos(theta),2) + Fp * Mathf.Sin(theta)) + vk * Mathf.Sin(theta),2)));
//                 transform.position = new Vector3(positionList[positionList.Count-1][0] - upset * Mathf.Sin(theta), positionList[positionList.Count-1][1] + upset*Mathf.Cos(theta), 0f);
//                 transform.rotation = Quaternion.AngleAxis(rotationList[rotationList.Count-1], new Vector3(0,0,1));
//                 energySpend = t * Fp;
//             }
//             else
//             {
//                 timer.run = false;
//             }
//         }
//     }
// }
