# ====== CELL 5: View Generated Outputs ======

from IPython.display import Image, Video
from pathlib import Path
import os

print("=" * 70)
print("📸 View Generated Outputs")
print("=" * 70)

storage_base = Path("/content/unrestricted-ai-backend/storage")

# Check Images
print("\n🖼️  Generated Images:")
print("-" * 70)

img_dir = storage_base / "images"
if img_dir.exists():
    images = sorted(list(img_dir.glob("*.png")))
    
    if images:
        print(f"\n✅ Found {len(images)} image(s)\n")
        
        # Show latest 3 images
        for img_path in images[-3:]:
            print(f"\n📸 {img_path.name}")
            print(f"   Size: {img_path.stat().st_size / 1024 / 1024:.2f}MB")
            print(f"   Path: {img_path}")
            
            try:
                display(Image(str(img_path)))
            except Exception as e:
                print(f"   Error displaying: {e}")
    else:
        print("\n❌ No images found yet")
        print("   Run CELL 4 to generate an image")
else:
    print(f"\n❌ Directory not found: {img_dir}")

# Check Videos
print("\n\n🎬 Generated Videos:")
print("-" * 70)

vid_dir = storage_base / "videos"
if vid_dir.exists():
    videos = sorted(list(vid_dir.glob("*.mp4")))
    
    if videos:
        print(f"\n✅ Found {len(videos)} video(s)\n")
        
        # Show latest video
        latest_video = videos[-1]
        print(f"\n🎥 {latest_video.name}")
        print(f"   Size: {latest_video.stat().st_size / 1024 / 1024:.2f}MB")
        print(f"   Path: {latest_video}")
        
        try:
            display(Video(str(latest_video)))
        except Exception as e:
            print(f"   Error displaying: {e}")
    else:
        print("\n❌ No videos found yet")
        print("   Run: requests.post(BASE_URL + '/api/v1/generate/video/', ...)")
else:
    print(f"\n❌ Directory not found: {vid_dir}")

# List all files
print("\n\n📂 All Storage Contents:")
print("-" * 70)

if storage_base.exists():
    for item in sorted(storage_base.rglob("*")):
        if item.is_file():
            rel_path = item.relative_to(storage_base)
            size_mb = item.stat().st_size / 1024 / 1024
            print(f"  {rel_path} ({size_mb:.2f}MB)")
else:
    print("  Storage directory not found")

print("\n" + "=" * 70)
print("✅ CELL 5 COMPLETE")
print("=" * 70)

# How to use
print("""
📋 Next Steps:

1. Download outputs:
   - Right-click on image → Save image as
   - Right-click on video → Save video as

2. Generate more images:
   Paste in a new cell:
   
   import requests
   BASE_URL = "http://127.0.0.1:8000"
   
   r = requests.post(f'{BASE_URL}/api/v1/generate/image/',
       json={
           "prompt": "Your prompt here",
           "width": 768,
           "height": 768,
           "steps": 25
       })
   print(r.json())

3. Try different features:
   - Face swap: POST /api/v1/faceswap/
   - Video: POST /api/v1/generate/video/
   - LLM: POST /api/v1/llm/chat
   - NeRF: POST /api/v1/nerf/train

4. API Documentation:
   Open in browser: http://127.0.0.1:8000/docs

✅ Everything is working! Enjoy!
""")

print("=" * 70)
