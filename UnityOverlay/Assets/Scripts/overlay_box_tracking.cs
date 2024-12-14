using UnityEngine;

public class overlay_box_tracking : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    public GameObject boundingBox;

    // Update is called once per frame
    void Update()
    {
        Transform box_transform = boundingBox.transform;



        // Set the follower object's position and rotation to match the leader

        transform.position = box_transform.position;

        transform.rotation = box_transform.rotation;
        
    }
}
