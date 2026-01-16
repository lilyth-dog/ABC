// DigitalHumanTwin.Build.cs
// 언리얼 엔진 모듈 빌드 설정 파일
// 이 파일을 프로젝트의 Source/DigitalHumanTwin/ 폴더에 배치

using UnrealBuildTool;

public class DigitalHumanTwin : ModuleRules
{
    public DigitalHumanTwin(ReadTargetTarget Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        
        PublicDependencyModuleNames.AddRange(new string[] 
        { 
            "Core", 
            "CoreUObject", 
            "Engine",
            "HTTP",
            "Json",
            "JsonUtilities"
        });
        
        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "Slate",
            "SlateCore",
            "ApplicationCore"
        });
    }
}
