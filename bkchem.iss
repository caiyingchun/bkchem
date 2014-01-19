; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=BKChem
AppVerName=BKChem-0.14.0-pre4
OutputBaseFilename=bkchem-0.14.0-pre4
VersionInfoVersion=0.14.0.4
VersionInfoTextVersion=0.14.0-pre4
AppPublisher=Reinis Danne
AppPublisherURL=http://bkchem.zirael.org
AppSupportURL=http://bkchem.zirael.org
AppUpdatesURL=http://bkchem.zirael.org/bkchem
DefaultDirName={pf}\BKChem
DefaultGroupName=BKChem
AllowNoIcons=yes
LicenseFile=gpl.txt
Compression=lzma
SolidCompression=yes
SetupIconFile=images\icon.ico
PrivilegesRequired=none


[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\BKChem"; Filename: "{app}\bkchem\bkchem.exe"; WorkingDir: "{userdocs}"; IconFilename: "{app}\images\icon.ico"
Name: "{group}\{cm:UninstallProgram,BKChem}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\BKChem"; Filename: "{app}\bkchem\bkchem.exe"; Tasks: desktopicon; WorkingDir: "{userdocs}"; IconFilename: "{app}\images\icon.ico"

[Run]
Filename: "{app}\bkchem\bkchem.exe"; Description: "{cm:LaunchProgram,BKChem}"; WorkingDir: "{userdocs}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: Files; Name: "{app}\bkchem\tuning.pyc"
