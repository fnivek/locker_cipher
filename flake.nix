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

          locker-cypher = python.pkgs.buildPythonApplication {
            pname = "locker-cypher";
            version = "0.1.0";
            pyproject = false;

            src = ./.;

            propagatedBuildInputs = [
              python.pkgs.click
            ];

            installPhase = ''
              runHook preInstall

              mkdir -p $out/${python.sitePackages}
              cp -r locker_cypher $out/${python.sitePackages}/

              mkdir -p $out/bin
              cat > $out/bin/f3 <<EOF
              #!${python}/bin/python
              from locker_cypher.cli.f3 import main
              main()
              EOF
              chmod +x $out/bin/f3

              runHook postInstall
            '';

            nativeCheckInputs = [
              python.pkgs.click
            ];

            doCheck = true;

            checkPhase = ''
              runHook preCheck
              ${python}/bin/python -c "from locker_cypher.ciphers.f3 import f3_cipher; assert f3_cipher(12) == 97"
              $out/bin/f3 12 | grep 'F3: 12 --> 97'
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
            default = locker-cypher;
            f3 = locker-cypher;
          };

          apps = {
            default = {
              type = "app";
              program = "${locker-cypher}/bin/f3";
            };

            f3 = {
              type = "app";
              program = "${locker-cypher}/bin/f3";
            };
          };

          devShells.default = pkgs.mkShell {
            packages = [
              python
              python.pkgs.click
            ];
          };
        };
    };
}
