using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using Newtonsoft.Json.Linq; 
public class ApriltagVisual : MonoBehaviour
{
    public GameObject boundingBox; // Assign a colored paper-like object here
    public float paperThickness = 0.01f; // Thickness of the bounding box

    private UdpClient udpClient;
    private IPEndPoint endPoint;

    void Start()
    {
        // Set up UDP client
        udpClient = new UdpClient(5005);
        endPoint = new IPEndPoint(IPAddress.Parse("172.26.168.18"), 5005);

        // Configure the bounding box if it's set
        if (boundingBox != null)
        {
            boundingBox.transform.localScale = new Vector3(0.2159f, paperThickness, 0.2794f); // Letter size paper: 8.5" x 11"
            boundingBox.GetComponent<Renderer>().material.color = Color.blue; // Example color
        }
    }

    void Update()
    {
        try
        {
            if (udpClient.Available > 0)
            {
                byte[] data = udpClient.Receive(ref endPoint);
                string jsonMessage = Encoding.UTF8.GetString(data);

                // Parse JSON
                var parsedData = JObject.Parse(jsonMessage);
                Vector3 position = new Vector3(
                    (float)parsedData["position"]["x"],
                    (float)parsedData["position"]["y"],
                    (float)parsedData["position"]["z"]
                );

                // Parse rotation matrix
                var rotationMatrix = new Matrix4x4();
                var r = parsedData["rotation"].ToObject<float[,]>();
                rotationMatrix.SetRow(0, new Vector4(r[0, 0], r[0, 1], r[0, 2], 0));
                rotationMatrix.SetRow(1, new Vector4(r[1, 0], r[1, 1], r[1, 2], 0));
                rotationMatrix.SetRow(2, new Vector4(r[2, 0], r[2, 1], r[2, 2], 0));
                rotationMatrix.SetRow(3, new Vector4(0, 0, 0, 1));

                Quaternion rotation = Quaternion.LookRotation(
                    rotationMatrix.GetColumn(2),
                    rotationMatrix.GetColumn(1)
                );

                // Update the attached object's position and rotation
                transform.position = position;
                transform.rotation = rotation;

                // Update the bounding box if it exists
                if (boundingBox != null)
                {
                    boundingBox.transform.position = position;
                    boundingBox.transform.rotation = rotation;
                }
            }
        }
          catch (System.Exception e)
        {
            Debug.Log($"Error receiving or parsing data: {e.Message}");
        }
    }

    void OnDestroy()
    {
        udpClient.Close();
    }
}
