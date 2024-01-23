using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CurveDrawer : MonoBehaviour
{
    public LineRenderer lineRenderer;
    public List<Vector3> pointList = new List<Vector3>();
    public controller optimController;

    void Start()
    {
        pointList = optimController.position;
        DrawCurve();

        if (optimController.indexCircuit == 0)
        {
            lineRenderer.startWidth = 0.1f;
            lineRenderer.endWidth = 0.1f;
        }

        else if (optimController.indexCircuit == 1)
        {
            lineRenderer.startWidth = 0.03f;
            lineRenderer.endWidth = 0.03f;
        }

        else if (optimController.indexCircuit == 2)
        {
            lineRenderer.startWidth = 0.5f;
            lineRenderer.endWidth = 0.5f;
        }
    }

    void DrawCurve()
    {
        lineRenderer.positionCount = pointList.Count;

        for (int i = 0; i < pointList.Count; i++)
        {
            Vector3 position = pointList[i];
            lineRenderer.SetPosition(i, position);
        }

    }

}
