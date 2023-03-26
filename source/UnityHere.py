import os, subprocess, sys
import win32api

# 설치된 유니티 에디터 경로
unityEditorPath = os.path.join("C:", os.sep, "Program Files", "Unity", "Hub", "Editor")
unityProgramPath = os.path.join("Editor", "Unity.exe")

# 선택된 프로젝트 폴더 및 프로젝트 세팅 경로
projectPath = sys.argv[1] # "C:\Program Files\UnityHere\UnityHere.exey" "%1"
projectSettingsPath = os.path.join(projectPath, "ProjectSettings", "ProjectVersion.txt")
editorVersionKey = "m_EditorVersion"

# 프로젝트 버전 확인
version = None
versionList = []

if not os.path.isfile(projectSettingsPath):
    win32api.MessageBox(0, "유니티 프로젝트 폴더가 맞는지 확인해보세요.", "Unity Here", 48)
    sys.exit(1)

with open(projectSettingsPath, 'r') as f:
    lines = f.readlines()
    for line in lines:
        words = line.strip().split(': ')
        if len(words) == 2 and words[0] == editorVersionKey:
            version = words[1]

if version == None:
    assert("ProjectVersion.txt에서 " + editorVersionKey + "을 찾지 못하였습니다")

# 유니티 에디터 버전 확인
searchList = os.listdir(unityEditorPath)
for name in searchList:
    fullPath = os.path.join(unityEditorPath, name)
    if os.path.isdir(fullPath):
        versionList.append(name)

for v in versionList:
    if v == version:
        cmd = os.path.join(unityEditorPath, version, unityProgramPath) + ' -projectPath ' + '"' + projectPath + '"'
        subprocess.run(cmd)
        sys.exit(1)

win32api.MessageBox(0, "프로젝트 버전과 일치하는 Unity Editor를 찾지 못하였습니다.\nProject Version: " + version + "\nUnity Editor Versions: " + ", ".join(versionList) + "\nUnity Hub를 통해 버전을 변경하거나 버전에 맞는 에디터를 설치하세요.", "Unity Here", 16)