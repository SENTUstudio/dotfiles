return {
  -- Añadir LSP para Python
  {
    "neovim/nvim-lspconfig",
    opts = function(_, opts)
      -- Configurar Pyright con opciones personalizadas
      opts.servers = opts.servers or {}
      opts.servers.pyright = {
        settings = {
          python = {
            analysis = {
              typeCheckingMode = "basic",
              autoSearchPaths = true,
              useLibraryCodeForTypes = true,
              diagnosticMode = "workspace",
            },
          },
        },
      }

      --   -- Detectar entorno virtual automáticamente al abrir un archivo Python
      --   vim.api.nvim_create_autocmd("BufEnter", {
      --     pattern = "*.py",
      --     callback = function()
      --       local cwd = vim.fn.getcwd()
      --       local venvs = { "venv", ".venv", "env" } -- Carpetas comunes de entornos virtuales
      --       for _, venv in ipairs(venvs) do
      --         local venv_path = cwd .. "/" .. venv
      --         if vim.fn.isdirectory(venv_path) == 1 then
      --           vim.g.python3_host_prog = venv_path .. "/bin/python"
      --           vim.cmd("LspRestart") -- Reinicia el LSP para aplicar el entorno
      --           print("Entorno virtual detectado y configurado: " .. venv_path)
      --           return
      --         end
      --       end
      --     end,
      --   })
    end,
  },

  -- Configurar herramientas de formato para Python
  {
    "stevearc/conform.nvim",
    opts = {
      formatters_by_ft = {
        python = { "black", "ruff_format", "ruff_fix" },
      },
    },
  },

  -- -- Configurar linting con ruff
  -- {
  --   "mfussenegger/nvim-lint",
  --   opts = {
  --     linters_by_ft = {
  --       python = { "ruff" },
  --     },
  --   },
  -- },

  -- Debugger para Python
  {
    "mfussenegger/nvim-dap",
    dependencies = {
      "mfussenegger/nvim-dap-python",
      config = function()
        -- Usar el mismo Python configurado en el entorno virtual
        local venv_path = vim.g.python3_host_prog or "/usr/bin/python3"
        require("dap-python").setup(venv_path)
      end,
    },
  },

  -- Mejorar la experiencia de desarrollo con Treesitter
  {
    "nvim-treesitter/nvim-treesitter",
    opts = {
      ensure_installed = {
        "python",
      },
    },
  },
  -- Tester para python
  {
    "nvim-neotest/neotest",
    dependencies = {
      "nvim-neotest/nvim-nio",
      "nvim-lua/plenary.nvim",
      "antoinemadec/FixCursorHold.nvim",
      "nvim-treesitter/nvim-treesitter",
      "nvim-neotest/neotest-python",
    },
  },

  {
    "linux-cultist/venv-selector.nvim",
    dependencies = { "neovim/nvim-lspconfig", "nvim-telescope/telescope.nvim", "mfussenegger/nvim-dap-python" },
    opts = {
      -- Your options go here
      -- name = "venv",
      -- auto_refresh = false
    },
    event = "VeryLazy", -- Optional: needed only if you want to type `:VenvSelect` without a keymapping
    keys = {
      -- Keymap to open VenvSelector to pick a venv.
      { "<leader>vs", "<cmd>VenvSelect<cr>" },
      -- Keymap to retrieve the venv from a cache (the one previously used for the same project directory).
      { "<leader>vc", "<cmd>VenvSelectCached<cr>" },
    },
  },

  -- -- Comandos para gestionar entornos virtuales manualmente
  -- config = function()
  --   local function set_python_venv(venv_path)
  --     vim.g.python3_host_prog = venv_path .. "/bin/python"
  --     vim.cmd("LspRestart") -- Reinicia el LSP para aplicar el cambio
  --     print("Usando entorno virtual: " .. venv_path)
  --   end
  --
  --   -- Comando para seleccionar un entorno virtual manualmente
  --   vim.api.nvim_create_user_command("SelectVenv", function(args)
  --     set_python_venv(args.args)
  --   end, { nargs = 1 })
  --
  --   -- Comando para detectar automáticamente un entorno virtual
  --   vim.api.nvim_create_user_command("AutoDetectVenv", function()
  --     local cwd = vim.fn.getcwd()
  --     local venvs = { "venv", ".venv", "env" }
  --     for _, venv in ipairs(venvs) do
  --       local venv_path = cwd .. "/" .. venv
  --       if vim.fn.isdirectory(venv_path) == 1 then
  --         set_python_venv(venv_path)
  --         return
  --       end
  --     end
  --     print("No se encontró un entorno virtual en el proyecto.")
  --   end, {})
  -- end,
}
