import os
import subprocess
import argparse


class Tomcat:

#############init functions

    def __init__(self, appDir, backupDir, app, deployDir) -> None:
        self.appDir = appDir
        self.app = app
        self.deployDir = deployDir
        self.backupDir = backupDir



###################### BUILD
    def build(self):
        print('Building ' + self.app + '...')  
        buildResult = subprocess.run(['mvn', 'clean', 'package'], cwd='/home/vboxuser/birdReco/birdReco-app/', capture_output=True, text=True)   
        if "BUILD SUCCESS" in buildResult.stdout:
            print('BUILD SUCCESS')
        else: 
            print('Build failed')
            print(buildResult.stdout)
            print(buildResult.stderr)
            return


################ status functions

    def status(self) -> bool:
        print('Checking if tomcat is running...')
        result = subprocess.run(['systemctl', 'status', 'tomcat9'], capture_output=True, text=True)
        if "active (running)" in result.stdout:
            print('Tomcat is running')
            return True
        else:
            print('Tomcat is not running')
            return False
        
    def stop(self):
        print('Stopping tomcat...')
        os.system('sudo systemctl stop tomcat9')
        while self.status() == True:
            pass

    def start(self):
        print('Starting tomcat...')
        os.system('sudo systemctl start tomcat9')
        while self.status() == False:
            pass
            


######################

    def undeploy(self):
        try:
            print('Undeploying and backing up old version of ' + self.app + ' from ' + self.deployDir)
            os.system('sudo mv ' + self.deployDir + '/' + self.app + ' ' + self.backupDir)
        except FileNotFoundError:
            print('File not found')


    def deploy(self):
        print('Deploying ' + self.app + ' to ' + self.deployDir)
        if not os.path.exists(self.appDir + self.app):
                print(f'Error: {self.app} does not exist.')
                return
        os.system('sudo mv ' + self.appDir + self.app + ' ' + self.deployDir)
        print('Successfully deployed ' + self.app + ' to ' + self.deployDir)




def main():

     # Using argparse for command line arguments
    parser = argparse.ArgumentParser(description='Deploy app using Tomcat.')
    parser.add_argument('--appname', type=str, default='bird-reco-1.0.war', help='The name of the app to deploy (e.g., app_name.war)')
    parser.add_argument('--deployDir', type=str, default='/var/lib/tomcat9/webapps/', help='The directory where the app will be deployed')
    parser.add_argument('--backupDir', type=str, default='/var/lib/tomcat9/old/', help='The directory where older version of the app will be deployed')
    parser.add_argument('--appDir', type=str, default='/home/vboxuser/birdReco/birdReco-app/target/', help='The directory where the app is located (default is current directory)')

    args = parser.parse_args()
# Initialize a Tomcat instance
    tomcat_instance = Tomcat(args.appDir, args.backupDir, args.appname, args.deployDir)
        
        # Build the app
    tomcat_instance.build()
        # Check Tomcat status
    if tomcat_instance.status() == True:
        tomcat_instance.stop()

        # Backup the app
   

    if os.path.exists(tomcat_instance.deployDir + '/' + tomcat_instance.app):
        tomcat_instance.undeploy()   
        
        # Deploy the app
    tomcat_instance.deploy()

    tomcat_instance.start()

if __name__ == "__main__":
        main()
    

    