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
        tex = pkgs.texlive.combine {
          inherit (pkgs.texlive) scheme-basic enumitem geometry;
        };
      in
      {
        defaultPackage = pkgs.mkShell {
          buildInputs = with pkgs; [ tex python3 ];
        };
      }
    );
}
