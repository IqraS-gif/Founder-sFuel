import os
import asyncio
import sys

# --- DEBUGGING START ---
print("📂 Current Directory:", os.getcwd())
print("📂 Files in root:", os.listdir('.'))

if os.path.exists('app'):
    print("✅ 'app' folder found. Contents:", os.listdir('app'))
else:
    print("❌ 'app' folder NOT FOUND. Check casing (App vs app)!")

if os.path.exists('services'):
    print("⚠️ Found 'services' in root (it should be inside app!)")
from apify_client import ApifyClient
# Import your existing service instance
from app.services.evaluation_service import evaluation_service

def main():
    # 1. Initialize Apify Client
    # The token is automatically provided by the platform environment
    client = ApifyClient(token=os.getenv('APIFY_TOKEN'))
    
    # 2. Get Input from the default Key-Value store
    print("🚀 Fetching input...")
    default_kv_store_id = os.getenv('APIFY_DEFAULT_KEY_VALUE_STORE_ID')
    actor_input = client.key_value_store(default_kv_store_id).get_record('INPUT')['value']
    
    if not actor_input or 'startup_idea' not in actor_input:
        print("❌ Error: No startup_idea provided in input.")
        return

    startup_idea = actor_input.get('startup_idea')
    startup_name = actor_input.get('startup_name', 'Unnamed Startup')

    print(f"🧠 Analyzing startup: {startup_name}")

    # 3. Run Your Existing Gemini Logic
    # We reuse the exact same function from your FastAPI backend!
    try:
        results = evaluation_service.comprehensive_startup_evaluation(
            startup_idea=startup_idea,
            startup_name=startup_name
        )
        print("✅ Evaluation complete.")
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        results = {"error": str(e)}

    # 4. Push Results to Dataset
    default_dataset_id = os.getenv('APIFY_DEFAULT_DATASET_ID')
    client.dataset(default_dataset_id).push_items([results])
    print("💾 Results saved to dataset.")

if __name__ == '__main__':
    main()