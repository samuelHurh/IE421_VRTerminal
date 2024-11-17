using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Splines;

public class Packet : MonoBehaviour
{
    //A packet is a visual representation of the packet being transferred between exchanges
    // It holds data pertaining to the packet that can be brought up by selecting the packet in vr

    [SerializeField]
    private SplineAnimate mySplineAnimator;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void ReceiveSpline(Spline s) {
        //mySplineAnimator.Spline
    }
}
