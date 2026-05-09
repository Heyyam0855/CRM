package com.lms.app.ui.auth

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.inputmethod.EditorInfo
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import com.lms.app.R
import com.lms.app.databinding.FragmentLoginBinding
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class LoginFragment : Fragment() {

    private var _binding: FragmentLoginBinding? = null
    private val binding get() = _binding!!

    private val viewModel: LoginViewModel by viewModels()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentLoginBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Artıq login olubsa — bilavasitə dashboard-a keç
        if (viewModel.isAlreadyLoggedIn()) {
            navigateToDashboard()
            return
        }

        setupListeners()
        observeViewModel()
    }

    private fun setupListeners() {
        // Daxil ol düyməsi
        binding.btnLogin.setOnClickListener {
            performLogin()
        }

        // Klaviaturada "Done" düyməsi ilə de login et
        binding.etPassword.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) {
                performLogin()
                true
            } else false
        }

        // Qeydiyyat linkə basanda
        binding.tvRegister.setOnClickListener {
            findNavController().navigate(R.id.action_login_to_register)
        }

        // Şifrəni unutdum
        binding.tvForgot.setOnClickListener {
            // TODO: Şifrə sıfırlama ekranı
            showError("Şifrə sıfırlama tezliklə əlavə ediləcək")
        }
    }

    private fun performLogin() {
        val email = binding.etEmail.text.toString().trim()
        val password = binding.etPassword.text.toString().trim()
        viewModel.login(email, password)
    }

    private fun observeViewModel() {
        viewModel.loginState.observe(viewLifecycleOwner) { state ->
            when (state) {
                is LoginState.Idle -> {
                    hideLoading()
                    hideError()
                }
                is LoginState.Loading -> {
                    showLoading()
                    hideError()
                }
                is LoginState.Success -> {
                    hideLoading()
                    navigateToDashboard()
                }
                is LoginState.Error -> {
                    hideLoading()
                    showError(state.message)
                }
            }
        }
    }

    private fun navigateToDashboard() {
        findNavController().navigate(R.id.action_login_to_dashboard)
    }

    private fun showLoading() {
        binding.progressBar.visibility = View.VISIBLE
        binding.btnLogin.isEnabled = false
        binding.btnLogin.text = "Gözləyin..."
        binding.etEmail.isEnabled = false
        binding.etPassword.isEnabled = false
    }

    private fun hideLoading() {
        binding.progressBar.visibility = View.GONE
        binding.btnLogin.isEnabled = true
        binding.btnLogin.text = getString(R.string.login_button)
        binding.etEmail.isEnabled = true
        binding.etPassword.isEnabled = true
    }

    private fun showError(message: String) {
        binding.tvError.visibility = View.VISIBLE
        binding.tvError.text = message
    }

    private fun hideError() {
        binding.tvError.visibility = View.GONE
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

