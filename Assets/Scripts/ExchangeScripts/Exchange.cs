using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Splines;

public class Exchange : MonoBehaviour
{
    public int myId; //The dominant node in the relationship is the one with the lower id.
    public List<Exchange> myNeighbors;
    public List<Spline> mySendingSplines;

    public GameObject mySplineAttach;


    public Vector3 GetPosition() {
        return this.transform.position;
    }

    public void Awake() {
        //I'll draw the splines and set up animation in Start()
        //Awake runs before Start
        SetUpMySpline();
    }
    
    // Start is called before the first frame update
    void Start()
    {
        GenerateSplines();

    }

    private void SetUpMySpline() {
        mySplineAttach = this.transform.Find("SplineAttach")?.gameObject;
    }

    private void GenerateSplines() {
        for (int i = 0; i < myNeighbors.Count; i++) {
            //Draw spline to neighbor exchange
            Vector3 neighborSplineAttach = myNeighbors[i].mySplineAttach.transform.position;
            if (myId < myNeighbors[i].myId) {
                //spline from this exchange to its neighbor is above the one from its neighbor to this
                Vector3[] pts = new Vector3[4];
                pts[0] = mySplineAttach.transform.position;
                pts[1] = mySplineAttach.transform.position + new Vector3(0f,1f,0f);
                pts[2] = myNeighbors[i].mySplineAttach.transform.position + new Vector3(0f,1f,0f);
                pts[3] = myNeighbors[i].mySplineAttach.transform.position;

                GameObject SplineFromMe = new GameObject();
                SplineFromMe.transform.SetParent(this.transform);
                var splinePosContainer = SplineFromMe.AddComponent<SplineContainer>();
                Spline spline = splinePosContainer.Spline;

                for (int j = 0; j < 4; j++) {
                    spline.Add(new BezierKnot(pts[j]));
                }
                spline.Closed = true;
                mySendingSplines.Add(spline);
            } else {
                GameObject SplineFromMe = new GameObject();
                SplineFromMe.transform.SetParent(this.transform);
                var splinePosContainer = SplineFromMe.AddComponent<SplineContainer>();
                Spline spline = splinePosContainer.Spline;

                spline.Add(new BezierKnot(mySplineAttach.transform.position));
                spline.Add(new BezierKnot(myNeighbors[i].mySplineAttach.transform.position));
            }
        }
    }

    public IEnumerator TestSendPacket() {
        
        yield return new WaitForSeconds(0.75f);

        StartCoroutine(TestSendPacket());
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
