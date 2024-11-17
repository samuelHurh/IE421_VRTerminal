using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "OrderBookDataObject", menuName = "ScriptableObjects/OrderBookDataObject", order = 1)]
public class OrderBookDataObject : ScriptableObject
{
    string message;
    string symbol;
    float bid_price;
    int bid_size;
    
    
    // 
    // Start is called before the first frame update
    // void Start()
    // {
        
    // }

    // // Update is called once per frame
    // void Update()
    // {
        
    // }
}
