# Maintainer: snow-arc
pkgname=shroomie-git
pkgver=r22.f7545c4
pkgrel=1
pkgdesc="A friendly AUR package manager with a simple GUI"
arch=('x86_64')
url="https://github.com/snow-arc/shroomie"
license=('MIT')
depends=('python>=3.8' 'python-pip' 'python-pyqt6' 'python-pexpect' 'git' 'base-devel')
makedepends=('python-setuptools' 'python-wheel')
source=("git+${url}.git")
sha256sums=('SKIP')

pkgver() {
    cd "${srcdir}/shroomie"
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}
build() {
    cd "${srcdir}/shroomie"
    # ننشئ مجلد مؤقت لتثبيت الحزم
    mkdir -p "${srcdir}/python-packages"
    python -m pip install --no-deps --ignore-installed --target="${srcdir}/python-packages" pexpect>=4.9.0
}

package() {
    cd "${srcdir}/shroomie"
    
    # Create directories
    install -dm755 "${pkgdir}/usr/bin"
    install -dm755 "${pkgdir}/usr/lib/shroomie"
    
    # Copy Python packages from build, excluding PyQt6
    find "${srcdir}/usr" -type f -not -path '*/PyQt6*' -exec install -Dm644 {} "${pkgdir}/{}" \;
    
    # Copy project files
    cp -r components config models resources services ui utils "${pkgdir}/usr/lib/shroomie/"
    install -Dm755 main.py "${pkgdir}/usr/lib/shroomie/"
    install -Dm644 README.md "${pkgdir}/usr/share/doc/shroomie/README.md"
    install -Dm644 "${startdir}/requirements.txt" "${pkgdir}/usr/share/doc/shroomie/requirements.txt"
    
    # Create launcher script with python3
    cat > "${pkgdir}/usr/bin/shroomie" << EOF
#!/bin/sh
exec python3 /usr/lib/shroomie/main.py "\$@"
EOF
    chmod 755 "${pkgdir}/usr/bin/shroomie"
}
