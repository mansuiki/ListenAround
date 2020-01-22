using System.Collections;
using System.Collections.Generic;
using socket.io;
using UnityEngine;
using LitJson;


namespace Sample
{
    public class CapsuleManager : MonoBehaviour
    {
        private GameObject server;
        private Rigidbody rb;
        private JsonData quat;
        private JsonData acce;
        public float angle = 0;
        // Start is called before the first frame update
        void Start()
        {
            server = GameObject.Find("SocketManager");
            rb = gameObject.GetComponent<Rigidbody>();
        }

        // Update is called once per frame
        private void FixedUpdate()
        {
            
        }
        public void rotate(float x, float y, float z)
        {
            
            //transform.rotation = new Quaternion(x, y, z, w);
            float t = 60 + z ;
            z = t;
            transform.rotation = Quaternion.Euler(0, z, 0);
            //transform.rotation = Quaternion.Euler(0, transform.eulerAngles.z, 0);
            //transform.rotation = Quaternion.Euler(x, y, z);
        }

        public void walk(float x, float y, float z)
        {
            if (Mathf.Abs(x) < 0.05) x = 0;
            if (Mathf.Abs(y) < 0.05) y = 0;
            if (Mathf.Abs(z) < 0.05) z = 0;
            transform.Translate(10*x,10*y,10*z);
        }

        public void LocSet(float x, float z)
        {
            transform.position = new Vector3(1160 + z, transform.position.y, 840 - x);
        }

        private void OnCollisionEnter(Collision collision)
        {
            if (collision.gameObject.tag == "warningCollider") Debug.Log("Warning!");
        }
    }

}



