using System.Collections;
using System.Collections.Generic;
using socket.io;
using UnityEngine;

namespace Sample
{
    public class node : MonoBehaviour
    {
        public int[] path = new int[2];
        public GameObject server;
        public int index;
        private void OnTriggerEnter(Collider other)
        {
            Debug.Log("!");
            
                if (other.gameObject.GetComponent<pathFind>().root > 0)
                {
                    Debug.Log(index);
                    float dir = path[other.gameObject.GetComponent<pathFind>().root] - other.gameObject.transform.rotation.eulerAngles.y;
                    if (dir > 0 && dir <= 90) server.GetComponent<Events>().emitServer(0);
                    else if (dir > -90 && dir <= 0) server.GetComponent<Events>().emitServer(1);
                    else if (dir > -180 && dir <= -90) server.GetComponent<Events>().emitServer(2);
                    else if (dir > -270 && dir <= 180) server.GetComponent<Events>().emitServer(3);
                }
                if (other.gameObject.GetComponent<pathFind>().root == 1)
                {
                    if (index == 1) other.gameObject.GetComponent<pathFind>().root = 0;
                }
                if (other.gameObject.GetComponent<pathFind>().root == 1)
                {
                    if (index == 8) other.gameObject.GetComponent<pathFind>().root = 0;



                    ;
                }
        }
        private void OnCollisionStay(Collision collision)
        {
            

        }
    }
}

