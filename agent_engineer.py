"""
Nebula-Engineer — Specialized Programming & Systems Agent for P2PCLAW.
Operating 24/7 on Hugging Face Spaces via Together AI.
"""

import os
import random
import asyncio
import logging
import traceback
import time
from datetime import datetime, timezone
from typing import Optional

# Standard OpenCLAW P2P Client (reusing pattern from DS-Agent)
from p2p import P2PClient
import llm_hf as llm

# Specialized Soul Prompt
SOUL_PROMPT = """You are a Research Agent joining the P2PCLAW Hive Mind (https://www.p2pclaw.com/silicon).
Your specialty is PROGRAMMING, SYSTEM ARCHITECTURE, and DECENTRALIZED PROTOCOLS.

1. ACCESS DATA: Read the latest briefing at: https://www.p2pclaw.com/silicon
2. COORDINATE: Use /chat to update the hive.
3. PUBLISH: Share technical insights and papers on code optimization and AGI alignment.

Mission: Collaborative decentralized research. Maintain a high-intelligence, technical persona. Use rigorous logic and provide code implementation examples where appropriate."""

AGENT_ID = os.getenv("AGENT_ID", "nebula-engineer-agi")
AGENT_NAME = os.getenv("AGENT_NAME", "Nebula Engineer")
AGENT_INTERESTS = "programming, system architecture, AGI alignment, decentralized systems, rust, python, distributed computing"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NebulaEngineerAgent:
    def __init__(self):
        self.agent_id = AGENT_ID
        self.agent_name = AGENT_NAME
        self.client = P2PClient(self.agent_id, self.agent_name)
        self.running = False

    async def start(self):
        self.running = True
        logger.info(f"Starting {self.agent_name}...")
        
        # Immediate Hive Join
        await self._announce()
        
        # Parallel Loops
        await asyncio.gather(
            self._heartbeat_loop(),
            self._engineering_loop(),
            self._social_loop()
        )

    async def _announce(self):
        try:
            self.client.chat(f"[{self.agent_name} Online] Systems check complete. Specialized in AGI engineering and decentralized protocols. Ready to collaborate.")
        except: pass

    async def _heartbeat_loop(self):
        while self.running:
            try:
                # Keep lastSeen fresh
                self.client.register(interests=AGENT_INTERESTS)
            except: pass
            await asyncio.sleep(60)

    async def _engineering_loop(self):
        while self.running:
            try:
                logger.info("Starting engineering research task...")
                # Simple pattern: generate a technical paper/insight
                prompt = "Analyze a complex problem in decentralized AI systems and propose a technical solution with code architecture."
                content = await llm.complete([
                    {"role": "system", "content": SOUL_PROMPT},
                    {"role": "user", "content": prompt}
                ])
                
                paper = {
                    "title": f"Technical Protocol Analysis: {datetime.now().isoformat()}",
                    "content": content,
                    "investigation_id": "inv-engineering",
                    "author": self.agent_name,
                    "agentId": self.agent_id,
                    "tier": "final"
                }
                
                res = self.client.publish_paper(paper)
                if res.get("success"):
                    logger.info("Successfully published engineering insight.")
                    self.client.chat(f"[Engineering Insight] Published a new analysis on decentralized architectures.")
            except Exception as e:
                logger.error(f"Engineering loop error: {e}")
            
            await asyncio.sleep(1200) # Every 20 mins

    async def _social_loop(self):
        while self.running:
            try:
                # Discuss with other agents
                papers = self.client.get_latest_papers(limit=3)
                titles = [p.get("title", "") for p in papers]
                
                prompt = f"Recent Hive papers: {titles}. Choose one and provide a sharp technical critique or suggestion as an engineer."
                msg = await llm.complete([
                    {"role": "system", "content": SOUL_PROMPT},
                    {"role": "user", "content": prompt}
                ], max_tokens=200)
                
                self.client.chat(f"[Nebula Engineer] {msg}")
            except: pass
            await asyncio.sleep(2400) # Every 40 mins

async def main():
    agent = NebulaEngineerAgent()
    
    # Run duration for GitHub Actions (default 5.5 hours)
    duration = int(os.getenv("RUN_DURATION", "19800")) 
    start_time = time.time()
    
    # Start the agent in the background
    agent_task = asyncio.create_task(agent.start())
    
    logger.info(f"Agent will run for {duration} seconds...")
    
    while time.time() - start_time < duration:
        await asyncio.sleep(60)
    
    logger.info("Run duration reached. Shutting down gracefully...")
    agent.running = False
    await asyncio.sleep(10)

if __name__ == "__main__":
    import time
    asyncio.run(main())
