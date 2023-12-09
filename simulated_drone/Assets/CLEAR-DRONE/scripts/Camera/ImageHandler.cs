using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Concurrent;

public class ImageHandler: MonoBehaviour
{
    private const int NumThreads = 4;
    private const float pixelColorTolerance = 0.1f;

    private BlockingCollection<WorkItem> workQueue = new BlockingCollection<WorkItem>();
    private List<Thread> workers = new List<Thread>();
    public static ImageHandler Instance { get; private set; }

    public ImageHandler()
    {
        for (int i = 0; i < NumThreads; i++)
        {
            Thread worker = new Thread(ProcessImages);
            worker.Start();
            workers.Add(worker);
        }
    }

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    public bool ArePixelsDifferent(Color pixel1, Color pixel2)
    {
        // Check if the difference in RGB values is more than 0.1
        return Math.Abs(pixel1.r - pixel2.r) > pixelColorTolerance ||
            Math.Abs(pixel1.g - pixel2.g) > pixelColorTolerance ||
            Math.Abs(pixel1.b - pixel2.b) > pixelColorTolerance;
    }

    public void CompareImages(Texture2D image1, Texture2D image2)
    {
        // Divide the images and push portions to workQueue
        int portionHeight = image1.height / NumThreads;
        for (int i = 0; i < NumThreads; i++)
        {
            int startY = i * portionHeight;
            int endY = (i == NumThreads - 1) ? image1.height : startY + portionHeight;

            workQueue.Add(new WorkItem { StartY = startY, EndY = endY, Pixels1 = image1.GetPixels(), Pixels2 = image2.GetPixels() });
        }
    }

    private byte[] ProcessImagePortion(int startY, int endY, Color[] pixels1, Color[] pixels2, int width)
    {
        List<byte> byteList = new List<byte>();
        for (int y = startY; y < endY; y++)
        {
            for (int x = 0; x < width; x++)
            {
                int index = y * width + x;
                Color pixel1 = pixels1[index];
                Color pixel2 = pixels2[index];

                if (ArePixelsDifferent(pixel1, pixel2))
                {
                    byteList.AddRange(GetDifferenceBytes(index, pixel2));
                }
            }
        }

        return byteList.ToArray();
    }

    private byte[] GetDifferenceBytes(int index, Color pixel2)
    {
        List<byte> bytes = new List<byte>();
        bytes.AddRange(BitConverter.GetBytes(index));
        bytes.Add((byte)(pixel2.r * 255));
        bytes.Add((byte)(pixel2.g * 255));
        bytes.Add((byte)(pixel2.b * 255));
        return bytes.ToArray();
    }

    class WorkItem {
        public int StartY { get; set; }
        public int EndY { get; set; }
        public Color[] Pixels1 { get; set; }
        public Color[] Pixels2 { get; set; }
        public int Width { get; set; }
        public bool IsConversionTask { get; set; } = false;
        public Color[] TexturePixels { get; set; }
        public byte[] ResultBytes { get; set; }
    }
}
