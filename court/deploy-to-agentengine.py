#!/usr/bin/env python3
"""
Deploy script for court agent to Google Cloud Agent Engine.

This script deploys the court agent system to Google Cloud's Agent Engine
for production use.
"""

import os
import sys
import json
from pathlib import Path
import vertexai
from vertexai import agent_engines

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from court.agent import root_agent

def deploy_court_agent():
    """Deploy the court agent to Google Cloud Agent Engine."""
    
    # Configuration
    PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
    LOCATION = os.getenv('AGENT_ENGINE_LOCATION', 'us-central1')
    AGENT_NAME = 'Court_AGENT'
    
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")
    
    print(f"Deploying court agent to project: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    print(f"Agent name: {AGENT_NAME}")
    
    # Initialize Vertex AI with staging bucket
    STAGING_BUCKET = f"gs://{PROJECT_ID}-staging"
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STAGING_BUCKET
    )
    
    # Deploy using Vertex AI Agent Engines
    try:
        # Create remote agent using agent_engines
        remote_agent = agent_engines.create(
            root_agent,
            requirements=["google-cloud-aiplatform[agent_engines,adk]"],
            display_name=AGENT_NAME
        )
        
        print(f"✅ Successfully deployed court agent!")
        
        # Get agent information - the returned object might have different attributes
        agent_info = {}
        if hasattr(remote_agent, 'name'):
            agent_info['name'] = remote_agent.name
            print(f"Agent name: {remote_agent.name}")
        if hasattr(remote_agent, 'resource_name'):
            agent_info['resource_name'] = remote_agent.resource_name
            print(f"Resource name: {remote_agent.resource_name}")
        elif hasattr(remote_agent, 'name'):
            agent_info['resource_name'] = remote_agent.name
            print(f"Resource name: {remote_agent.name}")
        
        # Try to get other available attributes
        for attr in ['id', 'agent_id', 'display_name', 'create_time']:
            if hasattr(remote_agent, attr):
                agent_info[attr] = getattr(remote_agent, attr)
                print(f"{attr}: {getattr(remote_agent, attr)}")
        
        # Save deployment info
        deployment_info = {
            "project_id": PROJECT_ID,
            "location": LOCATION,
            "display_name": AGENT_NAME,
            **agent_info
        }
        
        # Convert datetime objects to strings for JSON serialization
        for key, value in deployment_info.items():
            if hasattr(value, 'isoformat'):  # datetime-like object
                deployment_info[key] = value.isoformat()
        
        with open("deployment_info.json", "w") as f:
            json.dump(deployment_info, f, indent=2)
        
        return remote_agent
        
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        raise

def undeploy_court_agent():
    """Remove the court agent deployment."""
    
    PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
    LOCATION = os.getenv('AGENT_ENGINE_LOCATION', 'us-central1')
    
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")
    
    print(f"Removing court agent deployment from project: {PROJECT_ID}")
    
    try:
        # Load deployment info
        if not os.path.exists("deployment_info.json"):
            print("❌ No deployment info found. Cannot undeploy.")
            return
        
        with open("deployment_info.json", "r") as f:
            deployment_info = json.load(f)
        
        # Delete the remote agent
        try:
            # Try different ways to get the agent based on available info
            if "agent_id" in deployment_info:
                remote_agent = agent_engines.get(
                    agent_id=deployment_info["agent_id"],
                    project_id=PROJECT_ID,
                    location=LOCATION
                )
            elif "name" in deployment_info:
                remote_agent = agent_engines.get(
                    name=deployment_info["name"],
                    project_id=PROJECT_ID,
                    location=LOCATION
                )
            elif "resource_name" in deployment_info:
                remote_agent = agent_engines.get(
                    name=deployment_info["resource_name"],
                    project_id=PROJECT_ID,
                    location=LOCATION
                )
            else:
                print("⚠ Warning: No agent identifier found in deployment info")
                return
                
            remote_agent.delete()
            print("✅ Remote agent deleted")
        except Exception as e:
            print(f"⚠ Warning: Failed to delete remote agent: {e}")
        
        # Remove deployment info file
        os.remove("deployment_info.json")
        print(f"✅ Successfully removed court agent deployment!")
        
    except Exception as e:
        print(f"❌ Undeployment failed: {str(e)}")
        raise

def main():
    """Main entry point for deployment script."""
    
    if len(sys.argv) < 2:
        print("Usage: python deploy.py [deploy|undeploy]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "deploy":
        deploy_court_agent()
    elif command == "undeploy":
        undeploy_court_agent()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python deploy.py [deploy|undeploy]")
        sys.exit(1)

if __name__ == "__main__":
    main()
