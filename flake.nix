# This flake gives you an environment where python and LaTeX are available, with the needed LaTeX packages preinstalled.
{
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-23.11;
    flake-utils.url = github:numtide/flake-utils;
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachSystem flake-utils.lib.allSystems (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        tex-with-packages = pkgs.texlive.combine {
          inherit (pkgs.texlive) scheme-basic
            # LaTeX packages are listed here
            enumitem geometry;
        };
      in
      {
        defaultPackage = pkgs.mkShell {
          buildInputs = with pkgs; [
            tex-with-packages # LaTeX with preinstalled packages
            python3
          ];
        };
      }
    );
}
