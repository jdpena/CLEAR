// XXX A. XXX. Distribution is unlimited.

// XXX supported XXXnder XXX of XXX for 
// XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions,
// findings, XXX 
// of the author(s) XXX the XXX 
// XXX of XXX for XXX and XXX.

// © 2023 XXX.

// XXX.XXX-11 Patent Rights - XXX (May 2014)

// The software/XXX-Is basis

// XXX.S. XXX with Unlimited Rights, as defined in XXX Part 
// XXX.XXX-XXX or 7014 (Feb 2014). Notwithstanding any copyright notice, 
// U.S. XXX rights in this work are defined by XXX XXX.XXX-XXX or 
// XXX XXX.XXX-7014 as detailed above. Use of this work other than as specifically
// XXX XXX.S. XXX may violate any copyrights that exist in this work.

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Text;
using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;

[System.Serializable]
//Simple object for holding server info
public class CommandData
{
    public string Command;
    public float[] velocities;
}

// DroneAgent primarily deals with the communication between 
//the drone and a remote server.It retrieves instructions from a server, 
//processes them, and then applies the corresponding actions to the drone.
// It also sends feedback information back to the server.
// This script uses VelocityControl to adjust the drone's motion
public class DroneAgent: MonoBehaviour {
	public VelocityControl velocityControl;
	public ProjectileLauncher launcher;

	public Transform clientObject;
	private string webUrl;
	public const float FORWARD_VELOCITY_RATE = 1.5f;
	public const float HORIZONTAL_VELOCITY_RATE = 1;
	public const float VERTICAL_VELOCITY_RATE = 1;
	public const float YAW_RATE = 0.5f;
	private Vector3 initialPos;
	private bool isFetching = false;
	private bool commandRunning = false;

	public const float resetTime = 0.5f;
	private float movementTimer = resetTime; 

	public void Start() {
		ServicePointManager.ServerCertificateValidationCallback = MyRemoteCertificateValidationCallback;

		webUrl = SupportFuncs.GetWebUrlFromConfig();

		Debug.Log(webUrl);

        if (webUrl == null)
        {
            Debug.LogError("Could not find or read the web URL from the config. Using a default value.");
        }

		InitializeAgent();
	}
	
	
	public bool MyRemoteCertificateValidationCallback(System.Object sender, 
													X509Certificate certificate, 
													X509Chain chain, 
													SslPolicyErrors sslPolicyErrors) {
        return true;
    }

	public void InitializeAgent() {
		initialPos = transform.position;
	}

	// FixedUpdate executes along side the physics engine.
    // Get instructions from the interface server
	public void FixedUpdate() {
		if (!isFetching) {
			//using the coroutine prevents the main thread from being
			//blocked while waiting for a server response. 
			StartCoroutine(GetInstructionInfo());
		}

		movementTimer -= Time.deltaTime;

		if (movementTimer <= 0f) {
			float[] arr = {0f,0f,0f,0f};
			useSentMovement(arr);
		}
	}

	//Applies sent movement controls to velocity
	public void useSentMovement(float[] act)
	{
		if (act.Length < 4)
		{
			Debug.LogError("Expected 4 actions, got: " + act.Length);
			return;
		}

		// Resetting the timer
		movementTimer = resetTime;
		// Velocity control based on received actions
		velocityControl.desired_vx = act[0] * FORWARD_VELOCITY_RATE;
		velocityControl.desired_vy = act[1] * HORIZONTAL_VELOCITY_RATE;
		velocityControl.desired_height += (act[2])*VERTICAL_VELOCITY_RATE;
		velocityControl.desired_yaw = act[3] * YAW_RATE;
	}


	string makeFeedbackString(string head, string content)
	{
		string value = (head + " is " + content);
		Debug.LogWarning(value);
		return value;
	}

	IEnumerator PostFeedback(string inputString)
	{
		Debug.Log("PostFeedback is being called with: " + inputString);
		string url = webUrl + "/feedbackUnity";
		string jsonPayload;

		if (inputString == "clientRotation?")
		{
			string clientRotationStr = string.Format("{0},{1},{2}",
				clientObject.rotation.eulerAngles.x,
				clientObject.rotation.eulerAngles.y,
				clientObject.rotation.eulerAngles.z);
			jsonPayload = "{\"feedback\": {\"clientRotation\": \"" + clientRotationStr + "\"}}";
		}
		else if (inputString == "ready?")
		{
			jsonPayload = "{\"feedback\": {\"ready\": \"ready\"}}";
		}
		else if (inputString == "state?")
		{
			string value = commandRunning ? "true" : "false";
			jsonPayload = "{\"feedback\": {\"commandOccuring\": \"" + value + "\"}}";
		}
		else
		{
			yield break; // Skip sending if none of the expected input strings match
		}

		UnityWebRequest www = new UnityWebRequest(url, "POST");
		byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonPayload);
		www.uploadHandler = new UploadHandlerRaw(bodyRaw);
		www.downloadHandler = new DownloadHandlerBuffer();
		www.SetRequestHeader("Content-Type", "application/json");
		www.certificateHandler = new MyCertificateHandler(); // Make sure this is implemented correctly

		yield return www.SendWebRequest();

		if (www.isNetworkError || www.isHttpError)
		{
			Debug.Log(www.error);
		}
		else
		{
			Debug.Log("JSON uploaded successfully");
		}
	}

	//Should have arguement to determine object to throw
	void throwObject(Vector2 point) 
	{
		// Access the ProjectileLauncher script
		// Simulate a click at the center of the screen
		launcher.SimulateClick(point);
	}

	void performAction(string inputString)
	{
		Debug.LogWarning("performing the action: " + inputString);

		if (inputString == "restart")
		{
			AgentReset();
		} 
		else if (inputString.Contains("throw")) {
			Vector2 throwPoint = SupportFuncs.ExtractTupleFromString(inputString);
			Debug.LogError(throwPoint);
			throwObject(throwPoint);
		} 
		else {
			Debug.LogError("The unknown command {" + inputString + 
			"} is being provided which is slowing down the robot");
		}
		
		//Ready to recceive additional commands
		commandRunning = false;
		StartCoroutine(PostFeedback("state?"));
	}

	//All server information is processed through here. 
	//Parses the data, checking for relevant keys. If a key exists, 
	//applies the data to the corresponding action or attribute
	void ProcessInstructionInfo(string json)
	{
		CommandData commandData = JsonUtility.FromJson<CommandData>(json);

		if (commandData.Command != null)
		{
			if (! commandData.Command.Contains("?")) {
				commandRunning = true;
				performAction(commandData.Command);
			} else {
				StartCoroutine(PostFeedback(commandData.Command));
			}
		} else
        {
			Debug.LogWarning("No command or query in the response.");
		}

		// Check for velocity data
		if (commandData.velocities != null && commandData.velocities.Length > 0)
		{
			useSentMovement(commandData.velocities);
		}
		else
		{
			Debug.LogWarning("No velocities in the response.");
		}
	}

	//Checks the server to see if any information is available.
	//It does not listen, it just checks, which needs to be updated for efficiency
	IEnumerator GetInstructionInfo()
	{
		isFetching = true;
		string url = webUrl + "/instructionInfo";
		UnityWebRequest www = UnityWebRequest.Get(url);
		www.certificateHandler = new MyCertificateHandler();

		// www.certificateHandler = sharedCertificateHandler; // Reuse the handler
		yield return www.SendWebRequest();

		if (www.isNetworkError || www.isHttpError)
		{
			Debug.Log(www.error);
		}
		else
		{
			ProcessInstructionInfo(www.downloadHandler.text);
		}

		isFetching = false;
	}

	//Resets position and states
	public void AgentReset()
	{
		transform.position = initialPos;
		transform.rotation = Quaternion.Euler (Vector3.forward);
		velocityControl.Reset();

	}

	void OnCollisionEnter(Collision other)
	{
		Debug.LogWarning ("-- COLLISION --");
		AgentReset();
	}

}