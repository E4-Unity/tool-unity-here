import os, sys
import configparser
import win32api
from tkinter import filedialog, Tk

#TODO 리팩토링
class ConfigManager():
    def __init__(self):
        rootPath = None
        if getattr(sys, 'frozen', False):
            # bundle
            rootPath = os.path.join(os.getenv('APPDATA'), 'UnityHere')
        else:
            # Python environment
            rootPath = os.curdir()
        self._configPath = os.path.join(rootPath, 'config', 'UnityHere.ini')
        self._pathSection = 'Path'
        self._pathKey = 'UnityEditorPath'

    def _readConfig(self):
        # No config file
        if not os.path.isfile(self._configPath):
            win32api.MessageBox(0, self._configPath, "Unity Here", 48)
            return None
        
        config = configparser.ConfigParser()
        config.read(self._configPath)

        # Nothing in config file
        if config == []:
            return None
        else:
            return config

    def getUnityEditorPath(self):
        config = self._readConfig()
        if config == None:
            return None
        
        # No path section
        if not self._pathSection in config:
            return None
        
        # No path key
        if self._pathKey in config[self._pathSection]:
            return config[self._pathSection][self._pathKey]
        else:
            return None
    
    def setUnityEditorPath(self, newPath):
        config = self._readConfig()
        if config == None:
            win32api.MessageBox(0, "Unity.ini 파일을 읽을 수 없습니다.", "Unity Here", 48)
            sys.exit(1)
            return
        
        # No path section
        if not self._pathSection in config:
            config.add_section(self._pathSection)
        
        config.set(self._pathSection, self._pathKey, newPath)

        with open(self._configPath, 'w') as f:
            config.write(f)

class UnityEditor():
    def __init__(self):
        # 설치된 유니티 에디터 경로
        self._defaultRootPath = os.path.join("C:", os.sep, "Program Files", "Unity", "Hub", "Editor")
        self._rootPath = self._defaultRootPath
        self._programPath = os.path.join("Editor", "Unity.exe")
        self._versions = []

    def scan(self):
        # Config 파일 확인
        configManager = ConfigManager()
        userPath = configManager.getUnityEditorPath()
        if userPath != None:
            self._rootPath = userPath

        if os.path.isdir(self._rootPath):
            searchList = os.listdir(self._rootPath)
            for name in searchList:
                fullPath = os.path.join(self._rootPath, name)
                if os.path.isdir(fullPath):
                    if "Editor" in os.listdir(fullPath):
                        self._versions.append(name)
        
        if len(self._versions) == 0:
            self._setUserPath(configManager)

    def _setUserPath(self, configManager):
        win32api.MessageBox(0, "경로 설정이 필요합니다.\n설치된 Unity 폴더를 선택해주세요", "Unity Here", 48)
        root = Tk()
        root.withdraw()
        userPath = filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title="Please select a Unity folder")
        userPath = self._checkUserPath(userPath)
        configManager.setUnityEditorPath(userPath)
        win32api.MessageBox(0, "경로 설정이 완료되었습니다.\n다시 실행해주세요.", "Unity Here", 64)
        sys.exit(1)

    def _checkUserPath(self, userPath):
        userPath = os.path.normpath(userPath)
        paths = userPath.split(os.sep)

        if paths[-1] == "Editor":
            return userPath
        elif paths[-1] == "Hub":
            return os.path.join(userPath, "Editor")
        elif paths[-1] == "Unity":
            return os.path.join(userPath, "Hub", "Editor")
        else:
           return os.path.join(userPath, "Unity", "Hub", "Editor")


    def getProgramPath(self, projectVersion):
        for version in self._versions:
            if version == projectVersion:
                return os.path.join(self._rootPath, projectVersion, self._programPath)
        
        return None
    
    def getVersions(self):
        return self._versions

class UnityProject():
    def __init__(self):
        self._path = None
        self._settingsPath = None
        self._editorVersionKey = "m_EditorVersion"
        self._version = None
    
    def _check(self):
        if not os.path.isfile(self._settingsPath):
            win32api.MessageBox(0, "유니티 프로젝트 폴더가 맞는지 확인해보세요.", "Unity Here", 48)
            sys.exit(1)

    def setPath(self, path):
        self._path = path
        self._settingsPath = os.path.join(self._path, "ProjectSettings", "ProjectVersion.txt")
        self._check()

    def scan(self):
        with open(self._settingsPath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                words = line.strip().split(': ')
                if len(words) == 2 and words[0] == self._editorVersionKey:
                    self._version = words[1]

        if self._version == None:
            assert("ProjectVersion.txt에서 " + self._editorVersionKey + "을 찾지 못하였습니다")
    
    def getVersion(self):
        return self._version
    
    def getPath(self):
        return self._path