import os, sys
import configparser
import win32api

class ConfigManager():
    def __init__(self):
        self._configPath = os.path.join(os.path.curdir, 'config', 'UnityHere.ini')
        self._pathSection = 'Path'
        self._pathKey = 'UnityEditorPath'

    def _readConfig(self):
        config = configparser.ConfigParser()
        config.read(self._configPath)

        # No config file
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
        self._programPath = os.path.join("Editor", "Unity.exe")
        self._versions = []

    def scan(self):
        searchList = os.listdir(self._defaultRootPath)
        for name in searchList:
            fullPath = os.path.join(self._defaultRootPath, name)
            if os.path.isdir(fullPath):
                self._versions.append(name)

    def getProgramPath(self, projectVersion):
        for version in self._versions:
            if version == projectVersion:
                return os.path.join(self._defaultRootPath, projectVersion, self._programPath)
        
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