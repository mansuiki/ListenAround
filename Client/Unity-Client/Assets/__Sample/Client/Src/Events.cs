using UnityEngine;
using System.Collections;
using socket.io;
using LitJson;
using System.IO;

namespace Sample {
    
    /// <summary>
    /// The basic sample to show how to send and receive messages.
    /// </summary>
    public class Events : MonoBehaviour {
        static string serverUrl = "http://192.168.43.187:33333";
        Socket socket;
        public JsonData quart;
        public int walks;
        public JsonData accer;
        public GameObject player;
        void Start() {
            socket = Socket.Connect(serverUrl);
            
            socket.On("getq", (string data) => {

                //Debug.Log(data);
                quart = JsonMapper.ToObject(data);
                player.GetComponent<CapsuleManager>().rotate(float.Parse(quart["roll"].ToString()),
                                                             float.Parse(quart["pitch"].ToString()),
                                                             float.Parse(quart["yaw"].ToString()));
                //player.GetComponent<CapsuleManager>().walk(float.Parse(quart[1]["x"].ToString()), float.Parse(quart[1]["y"].ToString()), float.Parse(quart[1]["z"].ToString()));
                quart.Clear();
            });

            socket.On("walk", (string data) =>
            {
                Debug.Log(data);
                player.transform.Translate(120,0,0);
                //walks = data;

            });

            socket.On("navigate", (string data) =>
            {
                Debug.Log(data);
                player.GetComponent<pathFind>().root = int.Parse(data);
                //walks = data;

            });

            /*socket.On("geto", (string data) => {
                Debug.Log(data);
                accer = JsonMapper.ToObject(data);
            float x = float.Parse(accer[0]["vx"].ToString());
            float y = float.Parse(accer[0]["vy"].ToString());
                player.GetComponent<CapsuleManager>().LocSet(x, y);
            });*/

            
        }

        public void emitServer(int value)
        {
            socket.Emit("putttt", value.ToString());
        }

        

    }

}