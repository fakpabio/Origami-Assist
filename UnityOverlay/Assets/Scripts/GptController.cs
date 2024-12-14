using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using Button = UnityEngine.UI.Button;


public class GptController : MonoBehaviour
{


    private UdpClient udpClient;
    private IPEndPoint endPoint;

    // public Button[] buttonsUnderCanvas;
    public GameObject Startm;
    public Button startButton;
    public GameObject Alignment;
    public Button alignmentButton;

    public GameObject ChooseProj;
    public Button chooseButton;

    public GameObject tree1;
    public Button tree1Button;

    public GameObject tree1v2;
    public Button tree1v2Button;

    public GameObject tree2;
    public Button tree2Button;

    public GameObject tree3;
    public Button tree3Button;

    public GameObject tree4;
    public Button tree4Button;

    public GameObject tree5;
    public Button tree5Button;

    public GameObject tree6;
    public Button tree6Button;

    public GameObject tree7;
    public Button tree7Button;

    public GameObject tree8;
    public Button tree8Button;


    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        // Set up UDP client
        udpClient = new UdpClient(6005);
        // IPAddress.Parse("172.26.168.18")
        // IPAddress.Parse("172.26.90.195")
        // IPAddress.Parse("172.0.0.1")
        endPoint = new IPEndPoint(IPAddress.Any, 0);
        
    }

    // Update is called once per frame
    void Update()
    {
        try
        {
            Debug.Log($"listening");
            if (udpClient.Available > 0) 
            {
                byte[] data = udpClient.Receive(ref endPoint);
                string jsonMessage = Encoding.UTF8.GetString(data); 

                Debug.Log($"Received message: {jsonMessage}");

                // check if the message is yes and invoke the button trigger
                if (jsonMessage.Trim().ToLower() == "yes") 
                {
    
                    if (Startm.activeSelf)
                    {
                        startButton.onClick.Invoke();
                        Debug.LogError("Valid button!");

                    }

                    else if (Alignment.activeSelf)
                    {
                        alignmentButton.onClick.Invoke();
                        Debug.LogError("Valid button!");

                    }

                    else if (ChooseProj.activeSelf)
                    {
                        chooseButton.onClick.Invoke();
                        Debug.LogError("Valid button!");

                    }

                    else if (tree1.activeSelf)
                    {
                        tree1Button.onClick.Invoke();
                        Debug.LogError("Valid button!");
                    }
                    else if (tree1v2.activeSelf){
                        tree1v2Button.onClick.Invoke();
                    }
                    else if (tree2.activeSelf){
                        tree2Button.onClick.Invoke();
                    }
                    else if (tree3.activeSelf){
                        tree3Button.onClick.Invoke();
                    }
                    else if (tree4.activeSelf){
                        tree4Button.onClick.Invoke();
                    }
                    else if (tree5.activeSelf){
                        tree5Button.onClick.Invoke();
                    }
                    else if (tree6.activeSelf){
                        tree6Button.onClick.Invoke();
                    }
                    else if (tree7.activeSelf){
                        tree7Button.onClick.Invoke();
                    }
                    else if (tree8.activeSelf){
                        tree8Button.onClick.Invoke();
                    }
                    
                    
                    



        
                }
                //else signify something to user to try again
            }
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Error receiving or processing data: {e.Message}");
        }
        
    }

    void OnDestroy()
    {
        if (udpClient != null)
        {
            udpClient.Close(); // Ensure the UDP client is closed when the script is destroyed
        }
    }
}
