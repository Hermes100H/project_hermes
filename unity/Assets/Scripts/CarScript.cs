using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarScript : MonoBehaviour
{
    // Start is called before the first frame update
    public Vector3 startPosition;
    public float startRotation;
    public List<Vector3> positionList;
    public List<float> speedList;
    public List<float> rotationList;
    public float g = 9.81f;
    public List<Vector3> positionCircuit;
    public List<float> accelerationProfile;
    public List<float> accelerationList;
    public TimerScript timer;
    public bool modePlayable;
    public BarScript accelerationBar;
    public controller optimController;
    public float upset;
    public float energySpend;
    public bool gameStarted;
    public EnergyBar energyBar;
    public bool gameOver;

    void Start()
    {
        Init();
    }

    void Init()
    {
        positionCircuit = optimController.position;
        accelerationProfile = optimController.csv.boost_profile;
        modePlayable = optimController.modePlayable;
        accelerationBar.modePlayable = modePlayable;
        float theta = startRotation * (Mathf.PI/180);
        transform.rotation = Quaternion.AngleAxis(startRotation, new Vector3(0,0,1));
        positionList.Add(startPosition);
        rotationList.Add(startRotation);
        accelerationList.Add(accelerationProfile[0]);
        speedList.Add(0f);

        if(optimController.indexCircuit == 0)
        {
            transform.localScale = new Vector3(4f, 4f, 0f);
            upset = 0.25f;
        }        
        else if(optimController.indexCircuit == 1)
        {
            transform.localScale = new Vector3(2f, 2f, 0f);
            upset = 0.1f;
        }

        else if (optimController.indexCircuit == 2)
        {
            transform.localScale = new Vector3(30f, 30f, 1f);
            upset = 0.5f;
        }
        transform.position = new Vector3(startPosition[0] - upset * Mathf.Sin(theta), startPosition[1] + upset *Mathf.Cos(theta), 0f);

        timer.select = 1;
        timer.run = false;
        gameStarted = false;
        gameOver = false;
    }

    float FindRelevantRoot(float r1, float r2)
    {
        float ret = -1000f;
        if (r1 > 0 && r2 > 0 && r1 > r2)
        {
            ret = r2;
        }
        else if (r1 > 0 && r2 > 0 && r2 > r1)
        {
            ret = r1;
        }
        else if (r1 < 0 && r2 > 0)
        {
            ret = r2;
        }
        else if (r2 < 0 && r1 > 0)
        {
            ret = r1;
        }
        else if (r1 < 0 && r2 < 0)
        {
            ret = -1000f;
        }
        return ret;
    }

    // Update is called once per frame
    void Update()
    {
        if (optimController.gameStarted)
        {
            if (timer.timer == 0f)
            {
                timer.run = true;
            }
            if (!modePlayable)
            {
                //if ((positionList[positionList.Count-1][0] < positionCircuit[positionCircuit.Count-2][0]) && (positionList[positionList.Count-1][0] >= positionCircuit[0][0]))
                if(timer.run == true)
                {
                    float xk = positionList[positionList.Count-1][0];
                    float yk = positionList[positionList.Count-1][1];
                    float vk = speedList[speedList.Count-1];
                    float thetak = rotationList[rotationList.Count-1] * (Mathf.PI/180);
                    float t = Time.deltaTime;
                    float Fp = accelerationList[accelerationList.Count-1];
                    accelerationBar.barValue = Fp;

                    int count = 0;
                    for (int i = 0; i < positionCircuit.Count; i++)
                    {
                        if (xk > positionCircuit[i][0])
                        {
                            count = i;
                        }
                    }

                    int count_search = 1;
                    float x_actual = xk;
                    float y_actual = yk;
                    float v_actual = vk;
                    float Fp_actual = Fp;
                    float next_x = 0;
                    float new_t = 0;
                    float Fpx = 0;
                    float Fpy = 0;
                    float vkx = 0;
                    float vky = 0;
                    float new_theta = thetak;
                    float sign = -1;
                    while(true)
                    {

                        if(count != positionCircuit.Count-count_search)
                        {
                            next_x = positionCircuit[count + count_search][0];
                        }
                        else
                        {
                            break;
                        }

                        float a = (-g/2) * Mathf.Cos(new_theta) * Mathf.Sin(new_theta) + Fp_actual * Mathf.Cos(new_theta);
                        float b = v_actual * Mathf.Cos(new_theta);
                        float c = x_actual - next_x;
                        float disc = b * b - 4 * a * c;

                        if (disc >= 0)
                        {
                            float root1 = (-b + Mathf.Sqrt(disc)) / (2 * a);
                            float root2 = (-b - Mathf.Sqrt(disc)) / (2 * a);

                            float root = FindRelevantRoot(root1, root2);
                            if (root > 0 && root < t)
                            {   Fpx += root * root * (Fp_actual * Mathf.Cos(new_theta) + (-g/2) * Mathf.Cos(new_theta) * Mathf.Sin(new_theta));
                                Fpy += root * root * (Fp_actual * Mathf.Sin(new_theta) + (g/2) * Mathf.Pow(Mathf.Cos(new_theta),2) - (g/2));
                                vkx += root * v_actual * Mathf.Cos(new_theta);
                                vky += root * v_actual * Mathf.Sin(new_theta);

                                new_t = t - root;
                                new_theta = Mathf.Atan((positionCircuit[count + count_search][1]-positionCircuit[count + count_search - 1][1])/(positionCircuit[count + count_search][0]-positionCircuit[count + count_search -1][0]));
                                x_actual = next_x;
                                y_actual = positionCircuit[count + count_search][1];
                                sign = Mathf.Sign(new_t * (-g * Mathf.Cos(new_theta) * Mathf.Sin(new_theta) + Fp_actual * Mathf.Cos(new_theta)) + v_actual * Mathf.Cos(new_theta));
                                v_actual = sign * Mathf.Sqrt(Mathf.Pow(new_t * (-g  * Mathf.Cos(new_theta) * Mathf.Sin(new_theta) + Fp_actual * Mathf.Cos(new_theta)) + v_actual *Mathf.Cos(new_theta),2) + Mathf.Pow(new_t * (-g + g * Mathf.Pow(Mathf.Cos(new_theta),2) + Fp_actual * Mathf.Sin(new_theta)) + v_actual * Mathf.Sin(new_theta),2));
                                Fp_actual = accelerationProfile[count + count_search];
                                t = new_t;
                                count_search += 1;
                            }
                            else
                            {
                                Fpx += t * t * (Fp_actual * Mathf.Cos(new_theta) + (-g/2) * Mathf.Cos(new_theta) * Mathf.Sin(new_theta));
                                Fpy += t * t * (Fp_actual * Mathf.Sin(new_theta) + (g/2) * Mathf.Pow(Mathf.Cos(new_theta),2) - (g/2));
                                vkx += t * v_actual * Mathf.Cos(new_theta);
                                vky += t * v_actual * Mathf.Sin(new_theta);
                                break;
                            }
                        }

                        else
                        {
                            Fpx += t * t * (Fp_actual * Mathf.Cos(new_theta) + (-g/2) * Mathf.Cos(new_theta) * Mathf.Sin(new_theta));
                            Fpy += t * t * (Fp_actual * Mathf.Sin(new_theta) + (g/2) * Mathf.Pow(Mathf.Cos(new_theta),2) - (g/2));
                            vkx += t * v_actual * Mathf.Cos(new_theta);
                            vky += t * v_actual * Mathf.Sin(new_theta);
                            break;
                        }
                    }

                    float x = Fpx + vkx + xk;
                    float y = Fpy + vky + yk;
                    if (x > positionCircuit[positionCircuit.Count-1][0])
                    {
                        x = positionCircuit[positionCircuit.Count-1][0];
                        y = positionCircuit[positionCircuit.Count-1][1];
                    }
                    else if (x < positionCircuit[0][0])
                    {
                        x = positionCircuit[0][0];
                        y = positionCircuit[0][1];
                    }
                    positionList.Add(new Vector3(x,y,0f));

                    accelerationList.Add(Fp_actual);
                    new_theta = Mathf.Atan((positionCircuit[count + count_search][1]-positionCircuit[count + count_search - 1][1])/(positionCircuit[count + count_search][0]-positionCircuit[count + count_search -1][0]));
                    if (count != positionCircuit.Count)
                    {
                        rotationList.Add((180/Mathf.PI) * new_theta);
                    }
                    sign = Mathf.Sign(t * (-g * Mathf.Cos(new_theta) * Mathf.Sin(new_theta) + Fp_actual * Mathf.Cos(new_theta)) + v_actual * Mathf.Cos(new_theta));
                    speedList.Add(sign * Mathf.Sqrt(Mathf.Pow(t * (-g  * Mathf.Cos(new_theta) * Mathf.Sin(new_theta) + Fp_actual * Mathf.Cos(new_theta)) + v_actual *Mathf.Cos(new_theta),2) + Mathf.Pow(t * (-g + g * Mathf.Pow(Mathf.Cos(new_theta),2) + Fp_actual * Mathf.Sin(new_theta)) + v_actual * Mathf.Sin(new_theta
                    ),2)));
                    transform.position = new Vector3(positionList[positionList.Count-1][0] - upset * Mathf.Sin(new_theta), positionList[positionList.Count-1][1] + upset*Mathf.Cos(new_theta), 0f);
                    transform.rotation = Quaternion.AngleAxis(rotationList[rotationList.Count-1], new Vector3(0,0,1));
                }

                if (positionList[positionList.Count-1][0] == positionCircuit[positionCircuit.Count-1][0])
                {
                    timer.run = false;
                }
                else if (positionList[positionList.Count-1][0] == positionCircuit[0][0])
                {
                    timer.run = false;
                }
            }

            if (modePlayable)
            {
                //if ((positionList[positionList.Count-1][0] < positionCircuit[positionCircuit.Count-2][0]) && (positionList[positionList.Count-1][0] >= positionCircuit[0][0]))
                if (timer.run == true)
                {
                    float energyDisp = energyBar.energy.energyRemaining;
                    if (energyDisp == 0)
                    {
                        accelerationBar.bar.value = 0;
                    }

                    float xk = positionList[positionList.Count-1][0];
                    float yk = positionList[positionList.Count-1][1];
                    float vk = speedList[speedList.Count-1];
                    float thetak = rotationList[rotationList.Count-1] * (Mathf.PI/180);
                    float t = Time.deltaTime;
                    float Fp = accelerationBar.barValue;
                    accelerationBar.barValue = Fp;

                    int count = 0;
                    for (int i = 0; i < positionCircuit.Count; i++)
                    {
                        if (xk > positionCircuit[i][0])
                        {
                            count = i;
                        }
                    }

                    int count_search = 1;
                    float x_actual = xk;
                    float y_actual = yk;
                    float v_actual = vk;
                    float Fp_actual = Fp;
                    float next_x = 0;
                    float new_t = 0;
                    float Fpx = 0;
                    float Fpy = 0;
                    float vkx = 0;
                    float vky = 0;
                    float new_theta = thetak;
                    float sign = -1;
                    float e = 0;
                    while(true)
                    {

                        if(count != positionCircuit.Count-count_search)
                        {
                            next_x = positionCircuit[count + count_search][0];
                        }
                        else
                        {
                            break;
                        }

                        float a = (-g/2) * Mathf.Cos(new_theta) * Mathf.Sin(new_theta) + Fp_actual * Mathf.Cos(new_theta);
                        float b = v_actual * Mathf.Cos(new_theta);
                        float c = x_actual - next_x;
                        float disc = b * b - 4 * a * c;

                        if (disc >= 0)
                        {
                            float root1 = (-b + Mathf.Sqrt(disc)) / (2 * a);
                            float root2 = (-b - Mathf.Sqrt(disc)) / (2 * a);

                            float root = FindRelevantRoot(root1, root2);
                            if (root > 0 && root < t)
                            {   Fpx += root * root * (Fp_actual * Mathf.Cos(new_theta) + (-g/2) * Mathf.Cos(new_theta) * Mathf.Sin(new_theta));
                                Fpy += root * root * (Fp_actual * Mathf.Sin(new_theta) + (g/2) * Mathf.Pow(Mathf.Cos(new_theta),2) - (g/2));
                                vkx += root * v_actual * Mathf.Cos(new_theta);
                                vky += root * v_actual * Mathf.Sin(new_theta);
                                e += root * Fp_actual;

                                new_t = t - root;
                                new_theta = Mathf.Atan((positionCircuit[count + count_search][1]-positionCircuit[count + count_search - 1][1])/(positionCircuit[count + count_search][0]-positionCircuit[count + count_search -1][0]));
                                x_actual = next_x;
                                y_actual = positionCircuit[count + count_search][1];
                                sign = Mathf.Sign(new_t * (-g * Mathf.Cos(new_theta) * Mathf.Sin(new_theta) + Fp_actual * Mathf.Cos(new_theta)) + v_actual * Mathf.Cos(new_theta));
                                v_actual = sign * Mathf.Sqrt(Mathf.Pow(new_t * (-g  * Mathf.Cos(new_theta) * Mathf.Sin(new_theta) + Fp_actual * Mathf.Cos(new_theta)) + v_actual *Mathf.Cos(new_theta),2) + Mathf.Pow(new_t * (-g + g * Mathf.Pow(Mathf.Cos(new_theta),2) + Fp_actual * Mathf.Sin(new_theta)) + v_actual * Mathf.Sin(new_theta),2));
                                Fp_actual = accelerationBar.barValue;
                                t = new_t;
                                count_search += 1;
                            }
                            else
                            {
                                Fpx += t * t * (Fp_actual * Mathf.Cos(new_theta) + (-g/2) * Mathf.Cos(new_theta) * Mathf.Sin(new_theta));
                                Fpy += t * t * (Fp_actual * Mathf.Sin(new_theta) + (g/2) * Mathf.Pow(Mathf.Cos(new_theta),2) - (g/2));
                                vkx += t * v_actual * Mathf.Cos(new_theta);
                                vky += t * v_actual * Mathf.Sin(new_theta);
                                e += t * Fp_actual;
                                break;
                            }
                        }

                        else
                        {
                            Fpx += t * t * (Fp_actual * Mathf.Cos(new_theta) + (-g/2) * Mathf.Cos(new_theta) * Mathf.Sin(new_theta));
                            Fpy += t * t * (Fp_actual * Mathf.Sin(new_theta) + (g/2) * Mathf.Pow(Mathf.Cos(new_theta),2) - (g/2));
                            vkx += t * v_actual * Mathf.Cos(new_theta);
                            vky += t * v_actual * Mathf.Sin(new_theta);
                            e += t * Fp_actual;
                            break;
                        }
                    }

                    float x = Fpx + vkx + xk;
                    float y = Fpy + vky + yk;

                    energySpend = e;

                    if (x > positionCircuit[positionCircuit.Count-1][0])
                    {
                        x = positionCircuit[positionCircuit.Count-1][0];
                        y = positionCircuit[positionCircuit.Count-1][1];
                    }
                    else if (x < positionCircuit[0][0])
                    {
                        x = positionCircuit[0][0];
                        y = positionCircuit[0][1];
                    }
                    positionList.Add(new Vector3(x,y,0f));
                    if (count + count_search <= positionCircuit.Count-1)
                    {
                        new_theta = Mathf.Atan((positionCircuit[count + count_search][1]-positionCircuit[count + count_search - 1][1])/(positionCircuit[count + count_search][0]-positionCircuit[count + count_search -1][0]));
                    }
                    if (count != positionCircuit.Count)
                    {
                        rotationList.Add((180/Mathf.PI) * new_theta);
                    }
                    sign = Mathf.Sign(t * (-g * Mathf.Cos(new_theta) * Mathf.Sin(new_theta) + Fp_actual * Mathf.Cos(new_theta)) + v_actual * Mathf.Cos(new_theta));
                    speedList.Add(sign * Mathf.Sqrt(Mathf.Pow(t * (-g  * Mathf.Cos(new_theta) * Mathf.Sin(new_theta) + Fp_actual * Mathf.Cos(new_theta)) + v_actual *Mathf.Cos(new_theta),2) + Mathf.Pow(t * (-g + g * Mathf.Pow(Mathf.Cos(new_theta),2) + Fp_actual * Mathf.Sin(new_theta)) + v_actual * Mathf.Sin(new_theta
                    ),2)));
                    transform.position = new Vector3(positionList[positionList.Count-1][0] - upset * Mathf.Sin(new_theta), positionList[positionList.Count-1][1] + upset*Mathf.Cos(new_theta), 0f);
                    transform.rotation = Quaternion.AngleAxis(rotationList[rotationList.Count-1], new Vector3(0,0,1));
                }

                if (positionList[positionList.Count-1][0] == positionCircuit[positionCircuit.Count-1][0])
                {
                    timer.run = false;
                    gameOver = true;
                }
                else if (positionList[positionList.Count-1][0] == positionCircuit[0][0])
                {
                    timer.run = false;
                    gameOver = true;
                }
            }
        }
    }
}
