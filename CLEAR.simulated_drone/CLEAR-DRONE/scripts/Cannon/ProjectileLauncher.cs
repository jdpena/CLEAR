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

public class ProjectileLauncher : MonoBehaviour
{
    public GameObject projectilePrefab; // Drag your projectile prefab here in the inspector
    public float launchForce = 20f; // The magnitude of the force applied to the projectile
    public Camera mainCamera; // The camera used to calculate click positions. Typically your main camera

    public void SimulateClick(Vector2 screenPosition)
    {
        // Convert screen position to a ray
        Ray ray = mainCamera.ScreenPointToRay(screenPosition);
        RaycastHit hit;

        // Perform raycasting
        if (Physics.Raycast(ray, out hit))
        {
            // Calculate direction from the camera's position to the hit point
            Vector3 direction = hit.point - mainCamera.transform.position;

            // Normalize the direction
            direction.Normalize();

            // Launch the projectile in the calculated direction
            LaunchProjectile(direction);
        }
    }

    void LaunchProjectile(Vector3 direction)
    {
        // Instantiate a projectile at the camera's position
        GameObject projectile = Instantiate(projectilePrefab, mainCamera.transform.position, Quaternion.identity);

        // Set the projectile to the Projectile layer (Optional: see previous scripts for setup)
        projectile.layer = LayerMask.NameToLayer("Projectile");

        // Check if the projectile has a Rigidbody component
        Rigidbody rb = projectile.GetComponent<Rigidbody>();
        if (rb != null)
        {
            // Apply force to move the projectile
            rb.AddForce(direction * launchForce, ForceMode.Impulse);
        }
        else
        {
            Debug.LogError("Projectile does not have a Rigidbody component.");
        }
    }
}
