{
  description = "Locker cipher CLI tools packaged with pure Nix and flake-parts";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs =
    inputs@{
      flake-parts,
      ...
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
      ];

      perSystem =
        { pkgs, ... }:
        let
          python = pkgs.python312;

          locker-cipher = python.pkgs.buildPythonApplication {
            pname = "locker-cipher";
            version = "0.1.0";
            pyproject = false;

            src = ./.;

            propagatedBuildInputs = [
              python.pkgs.click
            ];

            nativeCheckInputs = [
              python.pkgs.pytest
            ];

            installPhase = ''
              runHook preInstall

              mkdir -p $out/${python.sitePackages}
              cp -r locker_cipher $out/${python.sitePackages}/

              mkdir -p $out/bin

              cat > $out/bin/f3 <<EOF
              #!${python}/bin/python
              from locker_cipher.cli.f3 import main
              main()
              EOF
              chmod +x $out/bin/f3

              cat > $out/bin/powerset-cipher <<EOF
              #!${python}/bin/python
              from locker_cipher.cli.powerset_cipher import main
              main()
              EOF
              chmod +x $out/bin/powerset-cipher

              runHook postInstall
            '';

            doCheck = true;

            checkPhase = ''
              runHook preCheck
              export PYTHONPATH="$PWD''${PYTHONPATH:+:''$PYTHONPATH}"
              pytest -q tests/
              runHook postCheck
            '';

            meta = with pkgs.lib; {
              description = "Small modular cipher CLI tools";
              mainProgram = "f3";
              license = licenses.mit;
              platforms = platforms.unix;
            };
          };
        in
        {
          packages = {
            default = locker-cipher;
            f3 = locker-cipher;
          };

          apps = {
            default = {
              type = "app";
              program = "${locker-cipher}/bin/f3";
            };

            f3 = {
              type = "app";
              program = "${locker-cipher}/bin/f3";
            };

            powerset-cipher = {
              type = "app";
              program = "${locker-cipher}/bin/powerset-cipher";
            };
          };

          devShells.default = pkgs.mkShell {
            packages = [
              python
              python.pkgs.click
              python.pkgs.pytest
            ];
            shellHook = ''
              export PYTHONPATH="$PWD''${PYTHONPATH:+:''$PYTHONPATH}"
              alias f3='python -m locker_cipher.cli.f3'
              alias powerset-cipher='python -m locker_cipher.cli.powerset'
            '';
          };
        };
    };
}
