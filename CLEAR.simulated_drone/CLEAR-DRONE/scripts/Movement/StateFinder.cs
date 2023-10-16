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

// The StateFinder class appears to be responsible for tracking and 
// providing the current state of the drone in terms of physical properties 
// such as position, orientation, velocities, inertia, and mass.
[System.Serializable]
public class StateFinder : MonoBehaviour {
	public float Altitude; // The current altitude from the zero position
	public Vector3 Angles;
	public Vector3 VelocityVector; // Velocity vector
	public Vector3 AngularVelocityVector; // Angular Velocity
	public Vector3 Inertia;
	public float Mass;

	private bool flag = true; // Only get mass and inertia once 

	public VelocityControl vc; // linked externally

	// Fetches the state of the drone including its current orientation, position, and velocities
	public void GetState() {
		Vector3 worldDown = vc.transform.InverseTransformDirection (Vector3.down);
		float Pitch = worldDown.z; // Small angle approximation
		float Roll = -worldDown.x; // Small angle approximation
		float Yaw = vc.transform.eulerAngles.y;

		Angles = new Vector3 (Pitch, Yaw, Roll);

		Altitude = vc.transform.position.y;

		VelocityVector = vc.transform.GetComponent<Rigidbody> ().velocity;
		VelocityVector = vc.transform.InverseTransformDirection (VelocityVector);

		AngularVelocityVector = vc.transform.GetComponent<Rigidbody> ().angularVelocity;
		AngularVelocityVector = vc.transform.InverseTransformDirection (AngularVelocityVector);

		if (flag) {
			Inertia = vc.transform.GetComponent<Rigidbody> ().inertiaTensor;
			Mass = vc.transform.GetComponent<Rigidbody> ().mass;
			flag = false;
		}
	}
	
    // Reset the state information
	public void Reset() {
		flag = true;
		VelocityVector = Vector3.zero;
		AngularVelocityVector = Vector3.zero;
		Angles = Vector3.zero;
		Altitude = 0.0f;

		enabled = true;
	}
}
