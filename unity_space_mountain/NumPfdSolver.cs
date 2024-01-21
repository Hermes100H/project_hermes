using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NumPfdSolver : MonoBehaviour{


    private float theta;
    private float mass;
    private float frictionCoeff;
    private float initialSpeed;
    private float boost;
    private float dx;
    private float g = 9.81f;
    private PositionFunction xFunction;



    public NumPfdSolver(float pMass, float pFricitonCoeff, float pInitialSpeed, float pBoost, float pDx, float pDy){
        SetConstants(pMass, pFricitonCoeff, pInitialSpeed, pBoost, pDx, pDy);
    }


    public void SetAngle(float dx, float dy){
        theta = Mathf.Atan(dy/dx);
    }

    public void SetConstants(float pMass, float pFrictionCoeff, float pInitialSpeed, float pBoost, float pDx, float pDy){
        
        SetAngle(pDx, pDy);
        mass = pMass;
        frictionCoeff = pFrictionCoeff;
        initialSpeed = pInitialSpeed;
        boost = pBoost;
        dx = pDx;
        SetPositionFunction();
    }

    private void SetPositionFunction(){

        float A = (Mathf.Pow(mass, 2)*(boost - g*Mathf.Sin(theta)) - mass*frictionCoeff*initialSpeed)/(Mathf.Pow(frictionCoeff, 2)*Mathf.Cos(theta));
        float lambda = mass*(boost-g*Mathf.Sin(theta))/frictionCoeff;
        float tau = mass / (frictionCoeff*Mathf.Cos(theta));

        xFunction = new PositionFunction(A, tau, lambda, dx);
    }




    public Solution Solve(){

        Debug.Log("Starting to solve");
        
        Solution tSolution = new Solution();

        if(theta > 0 && !(xFunction.HasValidRoot())) return tSolution;

        if(theta > 0 && xFunction.HasValidRoot()){

            xFunction.FindRootInterval();
            float tLeft = xFunction.tLeft;
            float tRight = xFunction.tRight;
            float slope = xFunction.slope;

            tSolution = DichotomyNumSolve(tLeft, tRight, slope);
        }

        if(theta < 0){ // Cas facile, où la voiture tombe grâce à la pente, donc atteint forcément le prochain point
            tSolution = DichotomyNumSolve(0f, 16f, 1f);
        }

        return tSolution;

    }


    public Solution DichotomyNumSolve(float tLeft, float tRight, float slope, float threshold=1e-9f){

        float tCurrent = (tRight + tLeft)/2.0f;
        float xCurrent = xFunction.Evaluate(tCurrent);
        
        while (Mathf.Abs(xCurrent) > threshold){

            if (slope*xCurrent < 0){
                tLeft = tCurrent;
                tCurrent = (tRight + tLeft)/2.0f;
            }
            else{
                tRight = tCurrent;
                tCurrent = (tRight + tLeft)/2.0f;
            }
            xCurrent = xFunction.Evaluate(tCurrent);

        }

        return new Solution(tCurrent);
    }



    private void Start(){

        Debug.Log("--------------------------------------- Start ---------------------------------------");


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



public class PositionFunction{


    private float A;
    private float tau;
    private float lambda;
    private float dx;


    private bool smiling;
    public float tInflexion;
    public float xInflexion;
    public float xOrigin;

    public float tLeft;
    public float tRight;
    public float slope;

    public Solution root;



    public PositionFunction(float pA, float pTau, float pLambda, float pDx){
        A = pA;
        tau = pTau;
        lambda = pLambda;
        dx = pDx;
        SetConstants();
    }


    private void SetConstants(){

        SetInflexionTime();
        SetInflexionPosition();
        SetSmiling();
    }


    public float Evaluate(float t){

        return A*(Mathf.Exp(-t/tau) -1) + lambda*t - dx;
    }


    public void SetOrigin(){
        xOrigin = Evaluate(0f);
    }
    private void SetInflexionTime(){

        float e = Mathf.Exp(1);
        tInflexion = tau*Mathf.Log(A/(tau*lambda), e);
    }

    private void SetInflexionPosition(){
        xInflexion = Evaluate(tInflexion);
    }

    private void SetSmiling(){
        smiling = Evaluate(tInflexion) < Evaluate(tInflexion + 1.0f);
    }

    public bool HasValidRoot(){

        if ( (xInflexion > 0) && (smiling) ) return false;
        if ( (xInflexion < 0) && (!smiling) ) return false;

        if ( (xInflexion < 0) && (tInflexion < 0) && (smiling) && (xOrigin > 0) )  return false;
        if ( (xInflexion > 0) && (tInflexion < 0) && (!smiling) && (xOrigin < 0) )  return false;

        return true;
    }


    public void FindRootInterval(){

        if ( (tInflexion < 0) && (xInflexion < 0) && smiling ){
            tLeft = 0f;
            tRight = 16f;
            slope = 1f;
            return;
        } 

        if ( (tInflexion > 0) && (xInflexion < 0) && smiling ){
            if (xOrigin < 0f){
                tLeft = tInflexion;
                tRight = tInflexion + 16f;
                slope = 1f;
            }
            else{
             tLeft = 0f;
             tRight = tInflexion;
             slope = -1f;
            }
            return;
        }

        if ( (tInflexion < 0) && (xInflexion > 0) && (!smiling) ){
            tLeft = 0;
            tRight = 16f;
            slope = -1f;
            return;
        }

        if ( (tInflexion > 0) && (xInflexion > 0) && (!smiling) ){
            if (xOrigin > 0f){
                tLeft = tInflexion;
                tRight = tInflexion + 16f;
                slope = -1f;
            }
            else{
                tLeft = 0f;
                tRight = tInflexion;
                slope = 1f;
            }
            return;
        }
        
    }


}
