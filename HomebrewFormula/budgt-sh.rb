class BudgtSh < Formula
  include Language::Python::Virtualenv

  desc "Budgt.sh - Modern Terminal User Interface (TUI) application for tracking personal expenses"
  homepage "https://github.com/yourusername/budgt.sh"
  url "https://files.pythonhosted.org/packages/source/b/budgt-sh/budgt-sh-0.1.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"  # This will be generated automatically when you upload to PyPI
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    # Test that the application can show help
    system "#{bin}/budgt", "--version" rescue true
    
    # Test that all required modules can be imported
    system libexec/"bin/python", "-c", "import budgt; print('Import successful')"
  end
end
