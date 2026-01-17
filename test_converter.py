import asyncio
import os
from pathlib import Path

from aiogram import Bot
from dotenv import load_dotenv

from bot.services import download_and_convert

load_dotenv()

TEST_FILES = [
    "CAACAgQAAxUAAWldEX2mU_rczlEGkb9rIjvNtJCfAAJlEwACDtQAAVE3iSiwFkmJozgE",
    "CAACAgIAAxUAAWldr055BZWRpEncmj5581hJbn90AAL4OAAC-BnISu4q4mU6JWMpOAQ",
    "CAACAgIAAxUAAWlpBz0HTq5di9GngXDs8kpqRaB9AAKhigACzOCJSPM-RVdUzdhWOAQ",
    "CAACAgIAAxUAAWlphVZ70al0PEwm8pxpBDg2OU-_AAJoAQACIjeOBJ1FPgl5K8mROAQ",
]


async def test_converter():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    
    print("🧪 Testing TGS converter with problematic files...\n")
    
    test_dir = Path("./test_results")
    test_dir.mkdir(exist_ok=True)
    
    for idx, file_id in enumerate(TEST_FILES, 1):
        print(f"[{idx}/{len(TEST_FILES)}] Testing file_id: {file_id[:20]}...")
        
        try:
            files, is_unsupported = await download_and_convert(file_id, bot)
            
            if not files:
                print(f"  ❌ No files generated")
                continue
            
            success = []
            failed = []
            
            for filename, data in files.items():
                if data and len(data) > 0:
                    success.append(filename.split('.')[-1])
                    output_path = test_dir / f"test{idx}_{filename}"
                    output_path.write_bytes(data)
                else:
                    failed.append(filename.split('.')[-1])
            
            print(f"  ✅ Success: {', '.join(success) if success else 'none'}")
            if failed:
                print(f"  ⚠️  Failed: {', '.join(failed)}")
            
            if is_unsupported:
                print(f"  ⚠️  Unsupported format")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()
    
    await bot.session.close()
    print(f"✅ Test complete! Results saved to {test_dir}/")


if __name__ == "__main__":
    asyncio.run(test_converter())
