using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using LitJson;
using System.IO;

public class testMove : MonoBehaviour
{
    string[] stringDatas = new string[300];
    JsonData[] parseDatas = new JsonData[300];
    public GameObject player;
    Rigidbody rb;
    // Start is called before the first frame update
    void Start()
    {
        string strPath = "Assets/Datas/mov2.txt";
        rb = player.GetComponent<Rigidbody>();
        ReadData(strPath);
        StartCoroutine(RunCoroutine());
    }

    public void ReadData(string FileName)
    {
        stringDatas = File.ReadAllLines(FileName);
        for (int i = 0; i < 300; i++)
        {
            parseDatas[i] = JsonMapper.ToObject(stringDatas[i]);
        }
        
        
        for (int i = 0; i < 300; i++)
        {
            Debug.Log(parseDatas[i][1]["x"]);
        }
    }
    
    IEnumerator RunCoroutine()
    {
        for(int i = 0; i < 300; i++)
        {
            player.transform.rotation = new Quaternion(float.Parse(parseDatas[i][0]["x"].ToString()),
                                                       float.Parse(parseDatas[i][0]["y"].ToString()),
                                                       float.Parse(parseDatas[i][0]["z"].ToString()),
                                                       float.Parse(parseDatas[i][0]["w"].ToString()));
            //player.transform.rotation = Quaternion.Euler(0, player.transform.eulerAngles.x, 0);

            player.transform.Translate(float.Parse(parseDatas[i][1]["x"].ToString()),
                                       float.Parse(parseDatas[i][1]["y"].ToString()),
                                       float.Parse(parseDatas[i][1]["z"].ToString()));

            yield return new WaitForSeconds(0.01f);
        }
    }
}
