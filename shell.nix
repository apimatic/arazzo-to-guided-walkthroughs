{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "arazzo-to-js-env";

  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.pyyaml
    pkgs.python3Packages.requests
  ];

  shellHook = ''
    echo "Welcome to the Arazzo to JavaScript Function Translator development shell!"
    echo "Python version: $(python3 --version)"
  '';
}
