using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OrderBookObjectManager : MonoBehaviour
{
    public List<OrderBookDataObject> OrderBookDataObjects;
    
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Insert(OrderBookDataObject o) {
        OrderBookDataObjects.Add(o);
    }

    public void Delete(string name) {}

    public void ClearAll() {}


}
