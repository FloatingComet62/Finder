{ pkgs, lib, config, inputs, ... }:

{
  packages = [ pkgs.git ];
  languages.python.enable = true;

  languages.python.venv.enable = true;
  languages.python.venv.requirements = builtins.readFile ./requirements.txt;

  dotenv.enable = true;
}
