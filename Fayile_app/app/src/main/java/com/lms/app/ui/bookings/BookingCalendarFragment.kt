package com.lms.app.ui.bookings

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.lms.app.databinding.FragmentBookingCalendarBinding
import com.lms.app.data.model.SlotResponse
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class BookingCalendarFragment : Fragment() {

    private var _binding: FragmentBookingCalendarBinding? = null
    private val binding get() = _binding!!
    private val viewModel: BookingViewModel by viewModels()

    private var selectedSlot: SlotResponse? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentBookingCalendarBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.rvSlots.layoutManager = LinearLayoutManager(requireContext())

        // Mövcud slotları yüklə
        viewModel.loadAvailableSlots()

        // Slotları müşahidə et
        viewModel.slots.observe(viewLifecycleOwner) { slots ->
            if (slots.isEmpty()) {
                Toast.makeText(
                    requireContext(),
                    "Hal-hazırda mövcud vaxt slotu yoxdur",
                    Toast.LENGTH_LONG
                ).show()
            }
            // TODO: SlotAdapter — Phase 2
        }

        // Slot seçiləndə təsdiq kartını göstər
        viewModel.isLoading.observe(viewLifecycleOwner) { loading ->
            binding.cardConfirm.visibility = if (selectedSlot != null && !loading) View.VISIBLE else View.GONE
            binding.btnConfirmBooking.isEnabled = !loading
            binding.btnConfirmBooking.text = if (loading) "Gözləyin..." else "Dərsi Təsdiqlə — 25 AZN"
        }

        // Dərs təsdiqlə düyməsi
        binding.btnConfirmBooking.setOnClickListener {
            selectedSlot?.let { slot ->
                viewModel.createBooking(
                    slotId = slot.id,
                    lessonType = "standard",
                    topic = ""
                )
            }
        }

        // Uğurlu rezervasiya
        viewModel.bookingSuccess.observe(viewLifecycleOwner) { success ->
            if (success) {
                Toast.makeText(
                    requireContext(),
                    "✅ Dərs uğurla rezerv edildi! 25 AZN",
                    Toast.LENGTH_LONG
                ).show()
                viewModel.resetBookingSuccess()
                findNavController().popBackStack()
            }
        }

        // Xəta
        viewModel.error.observe(viewLifecycleOwner) { msg ->
            if (!msg.isNullOrBlank()) {
                Toast.makeText(requireContext(), msg, Toast.LENGTH_SHORT).show()
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
