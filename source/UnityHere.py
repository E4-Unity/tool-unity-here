import os, subprocess, sys
import win32api

from classes import *

# 유니티 에디터 버전 확인
editor = UnityEditor()
editor.scan()

# 프로젝트 버전 확인
project = UnityProject()
project.setPath(sys.argv[1])
project.scan()

# 프로젝트 버전과 일치하는 유니티 에디터 검색
projectVersion = project.getVersion()
editorProgramPath = editor.getProgramPath(projectVersion)

if editorProgramPath == None:
    win32api.MessageBox(0, "프로젝트 버전과 일치하는 Unity Editor를 찾지 못하였습니다.\nProject Version: " + projectVersion + "\nUnity Editor Versions: " + ", ".join(editor.getVersions()) + "\nUnity Hub를 통해 버전을 변경하거나 버전에 맞는 에디터를 설치하세요.", "Unity Here", 16)
    sys.exit(1)

# 유니티 프로젝트 실행
cmd = editorProgramPath + ' -projectPath ' + '"' + project.getPath() + '"'
subprocess.run(cmd)