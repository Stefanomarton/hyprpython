{
  description = "HyprPython";

  inputs = { nixpkgs.url = "github:NixOS/nixpkgs"; };

  outputs = { nixpkgs, ... }:
    let pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in {
      # Specify the package
      packages.x86_64-linux.default =
        pkgs.python3Packages.buildPythonPackage rec {
          pname = "hyprpython";
          version = "0.1.0";

          src = ./.;

          nativeBuildInputs = with pkgs.python3Packages; [
            setuptools
            wheel
            plyer
          ];

          propagatedBuildInputs = with pkgs.python3Packages;
            [ ]; # Add dependencies here
        };

      # Dev shell
      devShells.x86_64-linux.default = pkgs.mkShell {
        packages = [
          pkgs.python3
          pkgs.python3Packages.setuptools
          pkgs.python3Packages.wheel
        ];
      };
    };
}
