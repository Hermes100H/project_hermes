using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NumPfdSolver : MonoBehaviour{


    public float sol;

    private float theta;
    private float mass;
    private float friction_coeff;
    private float initial_speed;
    private float boost;
    private float dx;
    private float g = 9.81f;
    private float A;
    private float tau;
    private float lambda;


    public void SetAngle(float dx, float dy){
        theta = Mathf.Atan(dy/dx);
    }

    public void SetConstants(float pMass, float pFriction_coeff, float pInitial_speed, float pBoost, float pDx, float pDy){
        
        SetAngle(pDx, pDy);
        mass = pMass;
        friction_coeff = pFriction_coeff;
        initial_speed = pInitial_speed;
        boost = pBoost;
        dx = pDx;
        SetEquationConstants();

    }

    private void SetEquationConstants(){

        A = (Mathf.Pow(mass, 2)*(boost - g*Mathf.Sin(theta)) - mass*friction_coeff*initial_speed)/(Mathf.Pow(friction_coeff, 2)*Mathf.Cos(theta));
        lambda = mass*(boost-g*Mathf.Sin(theta))/friction_coeff;
        tau = mass / (friction_coeff*Mathf.Cos(theta));
    }

    
    private float ComputeInflexionTime(){

        float e = Mathf.Exp(1);
        float tInflexion = tau*Mathf.Log(A/(tau*lambda), e);
        return tInflexion;
    }


    private float ComputeXEqualXnext(float t){
        float x  = A*(Mathf.Exp(-t/tau) -1) + lambda*t - dx;
        return x;
    }


    public Solution Solve(){
        
        Debug.Log("Starting to solve");
        float tSolution;

        if (theta < 0){tSolution = NumSolve();}

        else{

            float tInflexion = ComputeInflexionTime();
            if (ComputeXEqualXnext(tInflexion) < 0) {return new Solution();}

            tSolution = NumSolve(tInflexion);
        }

        return new Solution(tSolution);

    }


    public float NumSolve(){
        // Cas ou theta > 0, courbe de x croissante sur R+
        float threshold = 1e-9f;
        float tLeft = 0.0f;
        float tRight = 100.0f;
        float tCurrent = (tRight + tLeft)/2.0f;
        float xCurrent = ComputeXEqualXnext(tCurrent);
        
        while (xCurrent > threshold){

            Debug.Log("running");

            if (xCurrent < 0){
                tRight = tCurrent;
                tCurrent = (tRight + tLeft)/2.0f;
            }
            else{
                tLeft = tCurrent;
                tCurrent = (tRight + tLeft)/2.0f;
            }
            xCurrent = ComputeXEqualXnext(tCurrent);

        }

        return tCurrent;
    }

    public float NumSolve(float tRight){

        // Cas ou theta < 0, courbe de x croissante sur [0, tRight]
        float threshold = 1e-15f;
        float tLeft = 0.0f;
        float tCurrent = (tRight + tLeft)/2.0f;
        float xCurrent = ComputeXEqualXnext(tCurrent);
        
        while (xCurrent > threshold){

            if (xCurrent < 0){
                tRight = tCurrent;
                tCurrent = (tRight + tLeft)/2.0f;
            }
            else{
                tLeft = tCurrent;
                tCurrent = (tRight + tLeft)/2.0f;
            }
            xCurrent = ComputeXEqualXnext(tCurrent);

        }

        return tCurrent;
    }



    private void Start(){

        Debug.Log("Start funcitonzfmaiuzefliuzaeulicazui");

        float boost = 9.263267978358813f;
        float dx = 4.9913882356122485f;
        float dy = -0.25575537604623233f;
        SetConstants(1000f, 0.2f, 0f, boost, dx, dy );

        Solution s;

        s = Solve();


        sol = s.value;


    }



}


public class Solution{

    public bool exists;
    public float value;

    public Solution(float t){
        value = t;
        exists = true;
    }

    public Solution(){
        value = 100000f;
        exists = false;
    }

}